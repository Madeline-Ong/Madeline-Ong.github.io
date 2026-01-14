import sqlite3
import logging
from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
import json
import re
import secrets
import requests
import asyncio, asyncssh
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import traceback

# Initialize Flask app
app = Flask(__name__)

# Secret key for session management
app.secret_key = 'secret_key'

# For private key encryption 
ENCRYPTION_KEY_SIZE = 32 # AES-256 key size is 32
IV_SIZE = 16  # AES block size in bytes

# Configure session timeout (set to 20 minutes)
app.permanent_session_lifetime = timedelta(minutes=20)  # 20 minutes session timeout

# Add logging for debugging and important operations
logging.basicConfig(level=logging.DEBUG)

# Get the FastAPI URL from environment variable or use the default
VALIDATEURL = os.getenv('VALIDATEURL', 'https://fastapi:8050')
app.logger.info(f"Using VALIDATEURL: {VALIDATEURL}")
FASTAPI_URL = os.getenv("FASTAPI_URL", "https://v2-fastapi-1:9001/cve_lookup")
print(f"Using FASTAPI_URL: {FASTAPI_URL}")

# SQLite database connection
def get_db_connection():
    logging.debug('Connecting to the database')
    conn = sqlite3.connect('/app/db/AsmDB.db', check_same_thread=False, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

# Global variable to control if the redirection to test JSON is enabled
redirect_to_test = True  # Set this to True for using predefined JSONs, False for real CVE lookup

# Yolande - Serve the login page to allow logged in user's to enter the website.
@app.route('/')
def login():
    if 'user_id' in session:
        return redirect(url_for('main_page'))
    return render_template('login.html')

# Yolande - Handle the login form submission which requires the user's valid login credentials (Name and Password).
# Also ensure that the user that is logged in has their working status to 'Yes' in order for the user to be access the main page.
@app.route('/login', methods=['POST'])
def handle_login():
    name = request.form['name']
    password = request.form['password']

    # Ensure that both name and password are provided by the user
    if not name or not password:
        return jsonify({'success': False, 'message': 'Both Name and Password are required'})

    try:
        # Connect to the database.
        conn = get_db_connection()

        # Fetch the user information based on the provided name.
        user = conn.execute('SELECT * FROM User WHERE Name = ?', (name,)).fetchone()
        conn.close()

        # If a user record is found,
        if user:
            # Check the user's working status. If it is not Yes, log the login attempt and return the user and error message.
            if user['Working'] != 'Yes':
                error_message = "Please contact your in charge"
                log_user_action(user['User_ID'], 'Login Attempt', 'User not allowed to login. Working status is not "Yes".')
                return render_template('login.html', error_message=error_message)

            # Verify the provided password matches the stored hashed password.
            if check_password_hash(user['Password'], password):
                log_user_action(user['User_ID'], 'Login', 'Successful login')
                # Store necessary user details within the session.
                session['user_id'] = user['User_ID'] # Store the user's ID in the session.
                session['user_name'] = user['Name']  # Store the user's name in the session.
                session['user_role'] = user['Role']  # Store the user's role in the session.
                session['company'] = user['Company']  # Store the user's company in the session.
                # Redirect the user to the main page upon successful login.
                return redirect(url_for('main_page'))

        # If no user is found or the password is incorrect return error message.
        error_message = "Wrong Username or Password"
        return render_template('login.html', error_message=error_message)

    except sqlite3.Error as e:
        # Log any database errors for debugging.
        app.logger.error(f"Database error during login: {e}")
        error_message = "An error occurred while logging in. Please try again later."
        return render_template('login.html', error_message=error_message)

# Yolande - Serve the main page if user is logged in.
@app.route('/main_page')
def main_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Retrieve session variables.
    ip_range = session.get('ip_range')
    validation_result = session.pop('validation_result', None)
    show_confirmation_modal = session.pop('show_confirmation_modal', False)

    return render_template(
        'main_page.html',
        ip_range=ip_range,
        validation_result=validation_result,
        show_confirmation_modal=show_confirmation_modal
    )

# Yolande - Dropdown bar for main_page which shows the company's ip addresses and overall scans which will show in the charts.
@app.route('/get_ip_addresses', methods=['GET'])
def get_ip_addresses():
    try:
        # Check if the user is in session if not return an error message.
        if 'user_id' not in session:
            return jsonify({'error': 'User not logged in'}), 401

        user_id = session['user_id']
        conn = get_db_connection()

        # Fetch the user's company and role from the User table.
        user_data = conn.execute(
            'SELECT Company, Role FROM User WHERE User_ID = ?',
            (user_id,)
        ).fetchone()

        if not user_data:
            return jsonify({'error': 'User data not found'}), 404

        company_name = user_data['Company']
        user_role = user_data['Role']

        # if Role = Admin: Get all companies and their associated IPs.
        if user_role == 'Admin':
            company_data = conn.execute('''
                SELECT DISTINCT U.Company, MS.IP_Address
                FROM User U
                LEFT JOIN Madeline_Services MS ON U.User_ID = MS.User_ID
                ORDER BY U.Company
            ''').fetchall()

            # Organize data into a dictionary.
            companies = {}

            # Ensure "Overall - Admin" is always the first option.
            companies["Overall - All Companies"] = {"overall": "overall-admin", "ips": []}

            for row in company_data:
                company = row['Company']
                ip = row['IP_Address']

                if company not in companies:
                    companies[company] = {"overall": f"overall_{company}", "ips": []}

                if ip:
                    companies[company]["ips"].append(ip)

            # Convert the companies dictionary to an ordered structure with "Overall - Admin" first.
            ordered_companies = {" All Companies": companies.pop("Overall - All Companies")}
            ordered_companies.update(companies)
            logging.info(f'ordered_companies: {ordered_companies}')
            return jsonify({"role": "Admin", "companies": ordered_companies})

        else:
            # If Role != Admin: Fetch only IPs associated with the user's company.
            ip_addresses = conn.execute('''
                SELECT DISTINCT MS.IP_Address
                FROM Madeline_Services MS
                JOIN Yee_Xiang_CVE C ON MS.Services_ID = C.Services_ID
                JOIN User U ON MS.User_ID = U.User_ID
                WHERE U.Company = ?
            ''', (company_name,)).fetchall()

            # Convert query results to a list of IPs.
            ip_list = [ip['IP_Address'] for ip in ip_addresses]

            return jsonify({"role": "User", "ips": ip_list})

    except Exception as e:
        # Log the error for debugging.
        print(f"Error in /get_ip_addresses: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

# Yolande - Load severity data into main_page. It should show the severity data based on each of the ip address scanned.
@app.route('/severity_data', methods=['GET'])
def get_severity_data():
    ip_address = request.args.get('ip_address')  # Fetch the IP address from the query parameter.
    conn = get_db_connection()
    cursor = conn.cursor()

    scores = []
    try:
        if ip_address == "overall-admin":
            # Admin view: Fetch data for all companies.
            app.logger.info("Processing overall data for admin")

            query = '''
                SELECT c.CVSS_Score
                FROM Yee_Xiang_CVE c
                JOIN Madeline_Services s ON c.Services_ID = s.Services_ID
                JOIN User u ON s.User_ID = u.User_ID
            '''
            cursor.execute(query)

        elif ip_address.startswith("overall_"):
            # Extract company name from "overall_{company}".
            company_name = ip_address.split("_", 1)[1]

            if not company_name:
                app.logger.error(f"Invalid company name in IP address: {ip_address}")
                conn.close()
                return jsonify({"error": "Invalid company name"}), 400

            app.logger.info(f"Processing overall data for company: {company_name}")

            query = '''
                SELECT c.CVSS_Score
                FROM Yee_Xiang_CVE c
                JOIN Madeline_Services s ON c.Services_ID = s.Services_ID
                JOIN User u ON s.User_ID = u.User_ID
                WHERE LOWER(u.Company) = LOWER(?)
            '''
            cursor.execute(query, (company_name,))

        else:
            # Fetch data for a specific IP.
            query = '''
                SELECT c.CVSS_Score
                FROM Yee_Xiang_CVE c
                JOIN Madeline_Services s ON c.Services_ID = s.Services_ID
                WHERE s.IP_Address = ?
            '''
            cursor.execute(query, (ip_address,))

        # Process the fetched scores.
        for row in cursor.fetchall():
            score = row[0]
            if score is not None:  # Ensure the score is not NULL.
                try:
                    scores.append(float(score))  # Convert to float.
                except ValueError:
                    app.logger.warning(f"Invalid score encountered: {score}")

    except Exception as e:
        app.logger.error(f"Error fetching scores for IP {ip_address}: {e}")
        conn.close()
        return jsonify({"error": "Error processing scores"}), 500

    # If no scores are found for this IP address or company.
    if not scores:
        app.logger.info(f"No scores found for IP: {ip_address}")
        conn.close()
        return jsonify({
            "ip_address": ip_address,
            "average_score": 0,
            "severity_category": "None",
            "distribution": {"None": 0, "Low": 0, "Medium": 0, "High": 0, "Critical": 0}
        })

    # Calculate average score.
    average_score = sum(scores) / len(scores)

    # Determine severity category based on the average score.
    if average_score == 0:
        severity_category = "None"
    elif 0.1 <= average_score <= 3.9:
        severity_category = "Low"
    elif 4.0 <= average_score <= 6.9:
        severity_category = "Medium"
    elif 7.0 <= average_score <= 8.9:
        severity_category = "High"
    elif 9.0 <= average_score <= 10.0:
        severity_category = "Critical"

    # Initialise severity distribution.
    distribution = {"None": 0, "Low": 0, "Medium": 0, "High": 0, "Critical": 0}

    # Categorise scores into severity levels.
    for score in scores:
        if score == 0:
            distribution["None"] += 1
        elif 0.1 <= score <= 3.9:
            distribution["Low"] += 1
        elif 4.0 <= score <= 6.9:
            distribution["Medium"] += 1
        elif 7.0 <= score <= 8.9:
            distribution["High"] += 1
        elif 9.0 <= score <= 10.0:
            distribution["Critical"] += 1

    # Log the results.
    app.logger.info(f"IP Address: {ip_address}, Scores: {scores}")
    app.logger.info(f"Distribution: {distribution}")
    app.logger.info(f"Average Score: {average_score}, Severity Category: {severity_category}")

    conn.close()

    # Return the results as JSON.
    return jsonify({
        "ip_address": ip_address,
        "average_score": average_score,
        "severity_category": severity_category,
        "distribution": distribution
    })

# Yolande - Show severity data for overall of each company. 
# Admin should be able to see the overall of all companies and an overall of all scans done.
@app.route('/severity_data_overall', methods=['GET'])
def get_severity_data_overall():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Fetch user's company from the session.
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"error": "User not logged in"}), 403

        # Log the user ID for debugging.
        app.logger.info(f"User ID: {user_id}")

        query = '''
            SELECT Company FROM User WHERE User_ID = ?
        '''
        cursor.execute(query, (user_id,))
        user_company = cursor.fetchone()
        if not user_company:
            app.logger.error("User's company not found")
            return jsonify({"error": "User's company not found"}), 404
        user_company = user_company[0]

        # Log the company for debugging.
        app.logger.info(f"User's Company: {user_company}")

        # Fetch CVSS scores for the company.
        query = '''
            SELECT c.CVSS_Score
            FROM Yee_Xiang_CVE c
            JOIN Madeline_Services s ON c.Services_ID = s.Services_ID
            JOIN User u ON s.User_ID = u.User_ID
            WHERE u.Company = ?
        '''
        cursor.execute(query, (user_company,))
        scores = [row[0] for row in cursor.fetchall() if row[0] is not None]

        # Log fetched scores for debugging.
        app.logger.info(f"Fetched Scores: {scores}")

        if not scores:
            app.logger.info("No scores found for the user's company")
            return jsonify({
                "average_score": 0,
                "severity_category": "None",
                "distribution": {"None": 0, "Low": 0, "Medium": 0, "High": 0, "Critical": 0}
            })

        # Calculate average score and distribution.
        average_score = sum(scores) / len(scores)
        distribution = {"None": 0, "Low": 0, "Medium": 0, "High": 0, "Critical": 0}
        for score in scores:
            if score == 0:
                distribution["None"] += 1
            elif 0.1 <= score <= 3.9:
                distribution["Low"] += 1
            elif 4.0 <= score <= 6.9:
                distribution["Medium"] += 1
            elif 7.0 <= score <= 8.9:
                distribution["High"] += 1
            elif 9.0 <= score <= 10.0:
                distribution["Critical"] += 1

        # Log calculated average and distribution.
        app.logger.info(f"Average Score: {average_score}")
        app.logger.info(f"Distribution: {distribution}")

        return jsonify({
            "average_score": average_score,
            "severity_category": "None" if average_score == 0 else "Low" if average_score <= 3.9 else "Medium" if average_score <= 6.9 else "High" if average_score <= 8.9 else "Critical",
            "distribution": distribution
        })

    except Exception as e:
        app.logger.error(f"Error processing scores: {e}")
        return jsonify({"error": "Error processing scores"}), 500

    finally:
        conn.close()

# Yolande - Serve the signup page. 
# If user is logged in the session, redirect the user to the main page if not reutrn them back to the signup page.
@app.route('/signup')
def signup():
    if 'user_id' in session:
        return redirect(url_for('main_page'))
    return render_template('signup.html')

## Maria - to show the companies you can be signed up to 
@app.route('/signupDropdown', methods=['GET'])
def signup_dropdown():
    try:
        with get_db_connection() as conn:
            ## gets all company names except overall
            query = """
                SELECT DISTINCT Company
                FROM User
                WHERE Company IS NOT NULL AND Company != '' AND Company != 'Overall'
            """
            rows = conn.execute(query).fetchall()
            companies = [row['Company'] for row in rows]
            ## if theres no companies
            if not companies:
                return jsonify({"success": False, "error": "No companies found."}), 404
            return jsonify({"success": True, "data": companies})
    except sqlite3.Error as e:
        app.logger.error(f"Database error: {e}")
        return jsonify({"success": False, "error": "Database error."}), 500

# Yee Xiang - Handles the signup form submission by validating the user's input and storing it in the database.
@app.route('/signup', methods=['POST'])
def handle_signup():
    # Retrieve the user's input from the signup form
    name = request.form['name']
    password = request.form['password']
    company = request.form.get('Company')  # Get the selected company from the dropdown menu

    # Validate input: Check if any required field is empty
    if not name or not password or not company:
        error_message = 'Name, Password, and Company are required'
        return render_template('signup.html', error_message=error_message)

    # Validate name: Check if the name contains only allowed characters (letters, numbers, underscores, and spaces)
    name_regex = r'^[A-Za-z0-9_ ]+$'
    if not re.match(name_regex, name):
        error_message = 'Name can only contain letters, numbers, underscores, and spaces'
        return render_template('signup.html', error_message=error_message)

    # Validate password: Ensure it contains at least one uppercase letter, one number, and one special character
    password_regex = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@#$%&])[A-Za-z\d@#$%&]{8,}$'
    if not re.match(password_regex, password):
        error_message = 'Password must be at least 8 characters long and include at least one uppercase letter, one number, and one special character (@#$%&)'
        return render_template('signup.html', error_message=error_message)

    # Hash the password using Werkzeug's generate_password_hash to securely store it in the database
    hashed_password = generate_password_hash(password)

    try:
        # Connect to the database and check if the user already exists
        with get_db_connection() as conn:
            existing_user = conn.execute('SELECT * FROM User WHERE Name = ?', (name,)).fetchone()
            if existing_user:
                error_message = 'User already exists'
                return render_template('signup.html', error_message=error_message)

            # Insert new user data into the database (Name, Password, Company, Role, Working)
            conn.execute(''' 
                INSERT INTO User (Name, Password, Company, Role, Working) 
                VALUES (?, ?, ?, ?, ?)
            ''', (name, hashed_password, company, 'Worker', 'No'))
            conn.commit()

            # Get the user_id of the newly inserted user
            user_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]

            # Log the user's signup action (you can implement this function to log user actions)
            log_user_action(user_id, 'Signup', f"{name} signed up.")
        
        # Redirect to the login page after successful signup
        return redirect(url_for('login'))

    except sqlite3.Error as e:
        # Handle database errors
        error_message = 'Error signing up: ' + str(e)
        return render_template('signup.html', error_message=error_message)

# Yolande - Serve the assets page if user is logged in the session.
@app.route('/assets')
def assets():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']  # Get the current user's User_ID.
    user_role = session.get('user_role')  # Get the user's role.

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        if user_role == 'Admin':
            # Admin can see assets for all companies.
            raw_assets_data = cursor.execute('''
                SELECT 
                    u.Company, 
                    ma.Valid_IP_Range, ma.Assets_ID,
                    GROUP_CONCAT(ma.Active_Assets, ', ') AS Active_Assets
                FROM Maria_Assets ma
                JOIN User u ON ma.User_ID = u.User_ID
                GROUP BY u.Company, ma.Valid_IP_Range
            ''').fetchall()

            # Group assets by company for admins.
            company_assets = {}
            for row in raw_assets_data:
                company = row['Company']
                asset_id = row['Assets_ID']
                valid_ip_range = row['Valid_IP_Range']
                active_assets = row['Active_Assets'].split(', ') if row['Active_Assets'] else []
                deduplicated_assets = ', '.join(sorted(set(active_assets)))

                if company not in company_assets:
                    company_assets[company] = []

                company_assets[company].append({'Valid_IP_Range': valid_ip_range, 'Active_Assets': deduplicated_assets, 'Assets_ID': asset_id})
            
            logging.info(f'company_assets: {company_assets}')
             
            # Fetch all credentials - to show the diff ips (for various companies).
            # Sort by descending id to get latest credential stored for each ip.
            query = """
            SELECT 
                mc.Credential_ID, mc.User_ID, mc.IP_Address, mc.Credential
            FROM Madeline_Credentials mc
            ORDER BY mc.Credential_ID DESC
            """
            credentials_data = cursor.execute(query).fetchall()
            
            credentials = {}
            for credential in credentials_data:
                ip_addr = credential['IP_Address']
                cred = credential['Credential']
                logging.info(f'ip_addr: {ip_addr}, cred: {cred}')
                
                # Flag to break out of all loops.
                found = False 
                
                # Go through each set of assets.
                for assets in company_assets.values():
                    if found:
                        break  
                    
                    for asset in assets:
                        # Store Active Assets in a list.
                        for ip in asset['Active_Assets'].strip('\n').split(', '):
                            logging.info(f'ip check: {ip}')
                            if ip_addr == ip:
                                credentials[ip_addr] = 'Yes'
                                found = True 
                                break  
                            
                        if not found:
                            credentials[ip_addr] = 'No'
                        else:
                            break
                
                
            logging.info(f'credentials1: {credentials}')
            
            return render_template('assets.html', company_assets=company_assets, credentials_present=credentials, is_admin=True)

        else:
            # Get the company of the logged in user.
            user_company = cursor.execute('SELECT Company FROM User WHERE User_ID = ?', (user_id,)).fetchone()
            if not user_company:
                return "Error: User's company not found.", 400

            user_company = user_company['Company']
            logging.info(f'company: {user_company}')

            # Fetch assets for all users in the same company.
            raw_assets_data = cursor.execute('''
                SELECT 
                    ma.Valid_IP_Range, ma.Assets_ID,
                    GROUP_CONCAT(ma.Active_Assets, ', ') AS Active_Assets
                FROM Maria_Assets ma
                JOIN User u ON ma.User_ID = u.User_ID
                WHERE u.Company = ?
                GROUP BY ma.Valid_IP_Range
            ''', (user_company,)).fetchall()

            # Remove duplicate Active_Assets for each IP range.
            assets_data = []
            for row in raw_assets_data:
                valid_ip_range = row['Valid_IP_Range']
                asset_id = row['Assets_ID']
                active_assets = row['Active_Assets'].split(', ') if row['Active_Assets'] else []
                deduplicated_assets = ', '.join(sorted(set(active_assets)))
                assets_data.append({'Valid_IP_Range': valid_ip_range, 'Active_Assets': deduplicated_assets, 'Assets_ID': asset_id})

            logging.info(f'assets_data: {assets_data}')
            
            
            # Fetch credentials for the user's company.
            # Sort by descending id so get latest credential stored for each ip.
            query = """
            SELECT 
                mc.Credential_ID, mc.User_ID, mc.IP_Address, mc.Credential
            FROM Madeline_Credentials mc
            JOIN User u ON mc.User_ID = u.User_ID
            WHERE u.Company = ?
            ORDER BY mc.Credential_ID DESC
            """
            credentials_data = cursor.execute(query, (user_company,)).fetchall()
            
            credentials = {}
            for credential in credentials_data:
                ip_addr = credential['IP_Address']
                
                cred = credential['Credential']
                logging.info(f'ip_addr: {ip_addr}, cred: {cred}')
                
                # Flag to break out of all loops.
                found = False 
                
                # Go through each set of assets.
                for asset in assets_data:
                    if found:
                        break  # Break the outer loop if conditions are alr met.
                    
                    # Check each before storing Active Assets in a list.
                    for ip in asset['Active_Assets'].strip('\n').split(', '):
                        if ip_addr == ip:
                            credentials[ip_addr] = 'Yes'
                            found = True 
                            break  # Break the innermost loop.
                    if not found:
                        credentials[ip_addr] = 'No'
                
            logging.info(f'credentials_present: {credentials}')

            
            return render_template('assets.html', assets=assets_data, credentials_present=credentials, is_admin=False)

    except sqlite3.Error as e:
        app.logger.error(f"Database error: {e}")
        return "An error occurred while fetching assets.", 500

    finally:
        conn.close()

# Madeline - To remove assets from the assets page
@app.route('/remove_asset', methods=['POST'])
def remove_asset():
    # Get all necc info from the req 
    data = request.get_json()
    company = data.get('company')
    ip_range = data.get('ip_range')
    ip_to_remove = data.get('ip')
    
    # If dont have user_id, likely session timeout alr -> error 
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']  
    user_role = session.get('user_role')  
    
    # Company is blank for user, the way assets is passed into assets.html is diff from admin
    if not company and user_role == 'Admin':
        return jsonify({"success": False, "message": "Company is required."}), 400
    
    # Check if tried to send post w/o these params (eg intercept), then err 
    if not ip_range:
        return jsonify({"success": False, "message": "IP range is required."}), 400
    if not ip_to_remove:
        return jsonify({"success": False, "message": "IP to remove is required."}), 400

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # When passing data to assets page, doesnt show/store company for users. so have to get manually 
            #    Only for admin then stores & shows for all companies 
            company = cursor.execute('SELECT Company FROM User WHERE User_ID = ?', (user_id,)).fetchone()
            if not company:
                return "Error: User's company not found.", 400

            company = company['Company']
            logging.debug(f'company: {company}')

            logging.debug(f'ip_range: {ip_range}, ip_to_remove: {ip_to_remove}')
                
            # Get Active_Assets based on company & the ip_range 
            #    also applies for admin since they use the company that would be deleting from
            #    gets the asset_id for that ip_range, which would be whats updated when asset scan is run
            query = """
                SELECT ma.Assets_ID, ma.Active_Assets
                FROM User u
                JOIN Maria_Assets ma ON u.User_ID = ma.User_ID
                WHERE u.Company = ? AND ma.Valid_IP_Range = ?
                ORDER BY ma.Assets_ID DESC
                LIMIT 1;
            """
            
            # Should only get 1 result, just limit to be safe
            result = conn.execute(query, (company, ip_range)).fetchone()
            if result:
                result = dict(result)
                logging.info(f'result: {result}')
                asset_id = result['Assets_ID']
                active_assets = [ip.strip() for ip in result['Active_Assets'].split(',')] 
                
                logging.info(f'asset_id: {asset_id}, active_assets: {active_assets}')
            else:
                return jsonify({"success": False, "message": "Cannot retrieve from the db"}), 404
            
            # Check if the ip to remove is in the active assets - check jic 
            if ip_to_remove in active_assets:
                # Remove the IP from the Active_Assets 
                active_assets.remove(ip_to_remove)
                updated_assets = ', '.join(active_assets)
                cursor.execute('''
                        UPDATE Maria_Assets
                        SET Active_Assets = ?
                        WHERE Assets_ID = ?;
                    ''',
                    (updated_assets, asset_id)
                )
                
                # Deleting creds where same company as asset 
                cursor.execute('''
                    DELETE FROM Madeline_Credentials
                    WHERE IP_Address = ? AND User_ID IN (
                        SELECT User_ID
                        FROM User
                        WHERE Company = ?
                    );
                    ''',
                    (ip_to_remove, company)
                )
                
                # Delete services tied to that ip for the company 
                cursor.execute('''
                    DELETE FROM Madeline_Services
                    WHERE IP_Address = ? AND User_ID IN (
                        SELECT User_ID
                        FROM User
                        WHERE Company = ?
                    );
                    ''',
                    (ip_to_remove, company)
                )
                
                # Delete CVE vuln tied to that ip for the company
                cursor.execute('''
                    DELETE FROM Yee_Xiang_CVE
                    WHERE Assets_ID = ? AND User_ID IN (
                        SELECT User_ID
                        FROM User
                        WHERE Company = ?
                    );
                    ''',
                    (asset_id, company)
                )
                
                # Commit all changes to db - ensures changes actually made & saved 
                conn.commit()
                
            else:
                return jsonify({"success": False, "message": "IP not found in active assets / Unable to delete from db."}), 404
            
            # If can run till here means everything is working 
            return jsonify({"success": True, "message": "Successfully deleted related items"}), 200
            
    except sqlite3.Error as e:
        # Catch db err
        app.logger.error(f"Database error: {e}")
        return jsonify({"success": False, "message": "Database error occurred.", "details": str(e)}), 500
    except Exception as e:
        # Catch other unexpected err
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({"success": False, "message": "An unexpected error occurred.", "details": str(e)}), 500

# Yolande - Serve the services page if the user is in session. 
@app.route('/services')
def services():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']  # Get the logged-in user's User_ID.
    user_role = session.get('user_role')  # Get the user's role.

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        if user_role == 'Admin':
            # Admin view: Fetch all services grouped by company and IP.
            query = """
            SELECT 
                ms.Services_ID, ms.IP_Address, ms.Services, ms.Version, ms.Ports, 
                ms.Package_Name, ms.Process_Name, u.Company
            FROM Madeline_Services ms
            JOIN Maria_Assets ma ON ms.Assets_ID = ma.Assets_ID
            JOIN User u ON ma.User_ID = u.User_ID
            ORDER BY ms.Services_ID DESC
            """
            services_data = cursor.execute(query).fetchall()

            grouped_services = {}
            for service in services_data:
                company = service['Company']
                if company not in grouped_services:
                    grouped_services[company] = {}
                ip_address = service['IP_Address']
                if ip_address not in grouped_services[company]:
                    grouped_services[company][ip_address] = []
                # Avoid duplicate services for the same IP and port.
                if not any(s['Ports'] == service['Ports'] for s in grouped_services[company][ip_address]):
                    grouped_services[company][ip_address].append(service)

            # Check if no services exist and pass an empty dictionary to the template.
            if not grouped_services:
                grouped_services = {}

            return render_template('services.html', is_admin=True, grouped_services=grouped_services)

        else:
            # Employee view: Fetch services data for the user's company.
            user_company = cursor.execute(
                "SELECT Company FROM User WHERE User_ID = ?",
                (user_id,)
            ).fetchone()

            if not user_company:
                logging.error("Error: User's company not found.")
                return "Error: User's company not found.", 400

            user_company = user_company['Company']
            
            # Fetch services for the user's company.
            query = """
            SELECT 
                ms.Services_ID, ms.IP_Address, ms.Services, ms.Version, ms.Ports, 
                ms.Package_Name, ms.Process_Name
            FROM Madeline_Services ms
            JOIN Maria_Assets ma ON ms.Assets_ID = ma.Assets_ID
            JOIN User u ON ma.User_ID = u.User_ID
            WHERE u.Company = ?
            ORDER BY ms.Services_ID DESC
            """
            raw_services_data = cursor.execute(query, (user_company,)).fetchall()

            services_data = {}
            for service in raw_services_data:
                ip_address = service['IP_Address']
                if ip_address not in services_data:
                    services_data[ip_address] = {'all_services': [], 'credential_present': ''}

                # Avoid duplicate services for the same IP and port.
                if not any(s['Ports'] == service['Ports'] for s in services_data[ip_address]['all_services']):
                    service_info = {
                        'Services': service['Services'],
                        'Version': service['Version'],
                        'Ports': service['Ports'],
                        'Package_Name': service['Package_Name'],
                        'Process_Name': service['Process_Name']
                    }
                    services_data[ip_address]['all_services'].append(service_info)

            # Fetch credentials for the user's company.
            query = """
            SELECT 
                mc.Credential_ID, mc.User_ID, mc.IP_Address, mc.Credential
            FROM Madeline_Credentials mc
            JOIN User u ON mc.User_ID = u.User_ID
            WHERE u.Company = ?
            """
            credentials_data = cursor.execute(query, (user_company,)).fetchall()

            for credential in credentials_data:
                ip_addr = credential['IP_Address']
                if ip_addr in services_data:
                    services_data[ip_addr]['credential_present'] = 'Yes'
                else:
                    services_data[ip_addr] = {'all_services': [], 'credential_present': 'No'}

            # If no services found, pass an empty dictionary to the template.
            if not services_data:
                services_data = {}

            return render_template('services.html', is_admin=False, services_data=services_data)

    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
        return "An error occurred while fetching services.", 500

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return f"An unexpected error occurred: {e}", 500

    finally:
        conn.close()

#Yolande - Serve the cve page if the user is in session.
@app.route('/cve')
def cve():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']  # Get the logged in user's User_ID.
    user_role = session.get('user_role')  # Get the user's role.

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        if user_role == 'Admin':
            # Admins can see all CVEs grouped by company.
            query = """
            SELECT 
                yc.CVE_ID, yc.Cve_Number, yc.CVSS_Score, yc.Severity, yc.Reference_Link, yc.Publish_Date,
                ms.IP_Address, ms.Services, ms.Version, u.Company
            FROM Yee_Xiang_CVE yc
            JOIN Madeline_Services ms ON yc.Services_ID = ms.Services_ID
            JOIN User u ON yc.User_ID = u.User_ID
            """
            cve_data = cursor.execute(query).fetchall()

            # Group CVE data by company.
            grouped_cves = {}
            for cve in cve_data:
                company = cve['Company']
                if company not in grouped_cves:
                    grouped_cves[company] = []
                grouped_cves[company].append({
                    "CVE_ID": cve["CVE_ID"],
                    "Cve_Number": cve["Cve_Number"],
                    "CVSS_Score": cve["CVSS_Score"],
                    "Severity": cve["Severity"],
                    "Reference_Link": cve["Reference_Link"],
                    "IP_Address": cve["IP_Address"],
                    "Services": cve["Services"],
                    "Version": cve["Version"],
                    "Publish_Date": cve["Publish_Date"]
                })
                

            return render_template('cve.html', is_admin=True, grouped_cves=grouped_cves)

        else:
            # Get the company of the logged-in user.
            query = "SELECT Company FROM User WHERE User_ID = ?"
            user_company = cursor.execute(query, (user_id,)).fetchone()
            if not user_company or not user_company["Company"]:
                return jsonify({"success": False, "message": "User's company not found."}), 400

            user_company = user_company["Company"]

            # Fetch CVE data for all users in the same company.
            query = """
            SELECT 
                yc.CVE_ID, yc.Cve_Number, yc.CVSS_Score, yc.Severity, yc.Reference_Link, yc.Publish_Date,
                ms.IP_Address, ms.Services, ms.Version
            FROM Yee_Xiang_CVE yc
            JOIN Madeline_Services ms ON yc.Services_ID = ms.Services_ID
            JOIN User u ON yc.User_ID = u.User_ID
            WHERE u.Company = ?
            """
            cve_data = cursor.execute(query, (user_company,)).fetchall()

            # Process and structure the data.
            combined_cves = [
                {
                    "CVE_ID": cve["CVE_ID"],
                    "Cve_Number": cve["Cve_Number"],
                    "CVSS_Score": cve["CVSS_Score"],
                    "Severity": cve["Severity"],
                    "Reference_Link": cve["Reference_Link"],
                    "IP_Address": cve["IP_Address"],
                    "Services": cve["Services"],
                    "Version": cve["Version"],
                    "Publish_Date": cve["Publish_Date"]
                }
                for cve in cve_data
            ]

            return render_template('cve.html', is_admin=False, cves=combined_cves)

    except sqlite3.Error as e:
        app.logger.error(f"Database error: {e}")
        return jsonify({"success": False, "message": "Database error occurred.", "details": str(e)}), 500

    finally:
        conn.close()

## Maria - serve the account page
@app.route('/account')
def account():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT User_ID, Name FROM User')
    ##to display which user is logged on
    name = session.get('user_name', 'User')
    return render_template('account.html', name=name)

##Maria - changing user password
@app.route('/change_password', methods=['POST'])
def change_password():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'User not logged in'})
    ## gets old and new passwords
    data = request.get_json()
    old_password = data.get("oldPassword")
    new_password = data.get("newPassword")
    if not old_password or not new_password:
        return jsonify({'success': False, 'error': 'Both old and new passwords are required'})
    ## password complexities
    password_regex = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@#$%&])[A-Za-z\d@#$%&]{8,}$'
    if not re.match(password_regex, new_password):
        return jsonify({'success': False, 'error': 'Password must be at least 8 characters long and include at least one uppercase letter, one number, and one special character.'})
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            ## get old password hash
            cursor.execute("SELECT Password FROM User WHERE User_ID = ?", (session['user_id'],))
            user = cursor.fetchone()
            ## validates old password
            if not user or not check_password_hash(user["Password"], old_password):
                return jsonify({'success': False, 'error': 'Old password is incorrect'})
            if check_password_hash(user["Password"], new_password):
                return jsonify({'success': False, 'error': 'New password cannot be the same as the old password'})
            ## hash new password
            hashed_password = generate_password_hash(new_password)
            cursor.execute("UPDATE User SET Password = ? WHERE User_ID = ?", (hashed_password, session['user_id']))
            conn.commit()
        return jsonify({'success': True, 'message': 'Password updated successfully!'})
    except Exception as e:
        app.logger.error(f"Error occurred while changing password: {e}")
        return jsonify({'success': False, 'error': 'An unexpected error occurred. Please try again later.'})

# Yolande - Serve the admin management tab for logged in admins. 
@app.route('/admin')
def admin():
    # Restrict access to Admins only.
    if session.get('user_role') != 'Admin':
        return redirect(url_for('main_page'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch all users grouped by company.
    cursor.execute('SELECT Company, User_ID, Name, Role, Working FROM User ORDER BY Company, Role')
    users = cursor.fetchall()

    # Group users by company.
    companies = {}
    admins = []
    for user in users:
        if user["Role"] == "Admin":
            admins.append(user)  # Collect admins separately.
        else:
            if user["Company"] not in companies:
                companies[user["Company"]] = []
            companies[user["Company"]].append(user)

    conn.close()

    # Fetch the admin's name from the session.
    name = session.get('user_name', 'Admin')  # Default to 'Admin' if name is not in session.

    return render_template('admin.html', companies=companies, admins=admins, name=name)

## Maria -  add boss
@app.route('/addboss', methods=['POST'])
def addboss():
    try:
        ## get data
        boss_name = request.form.get('boss_name')
        company_name = request.form.get('company_name')
        password = request.form.get('password_boss')
        app.logger.debug(f"Received data: boss_name={boss_name}, company_name={company_name}, password={password}")
        ## secure password
        password_regex = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@#$%&])[A-Za-z\d@#$%&]{8,}$'
        if not re.match(password_regex, password):
            return jsonify({
                "success": False,
                "error": "Password must be at least 8 characters long and include at least one uppercase letter, one number, and one special character (@#$%&)."
            }), 400
        if not boss_name or not company_name or not password:
            return jsonify({"success": False, "error": "All fields are required."}), 400
        hashed_password = generate_password_hash(password)
        with get_db_connection() as conn:
            ## no duplicate users
            existing_user = conn.execute(""" 
                SELECT * FROM User WHERE Name = ?;
            """, (boss_name,)).fetchone()
            if existing_user:
                return jsonify({"success": False, "error": "Username already taken. Please choose a different one."}), 400
            conn.execute("""
                INSERT INTO User (Name, Password, Company, Role, Working)
                VALUES (?, ?, ?, 'Boss', 'Yes');
            """, (boss_name, hashed_password, company_name))
            conn.commit()
            log_user_action(None, 'Add Boss', f"Boss '{boss_name}' added to the company '{company_name}'.")
            return jsonify({"success": True, "message": "Boss added successfully."}), 201
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
        return jsonify({"success": False, "error": "Database error."}), 500
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({"success": False, "error": "An unexpected error occurred."}), 500

## Maria - get admin logs
@app.route('/adminlogs', methods=['GET'])
def adminlogs():
    ## only admins
    if session.get('user_role') != 'Admin':
        return redirect(url_for('main_page'))
    conn = get_db_connection()
    try:
        query = '''
        SELECT 
            Logs.Timestamp AS Time,
            User.Name AS UserName,
            User.Role AS UserRole,
            User.Company AS Company,
            Logs.Action_Type AS ActionType,
            Logs.Description AS Description
        FROM Logs
        LEFT JOIN User ON Logs.User_ID = User.User_ID
        ORDER BY Logs.Timestamp DESC;
        '''
        logs = conn.execute(query).fetchall()
        conn.close()
        return render_template('adminlogs.html', logs=logs)
    except Exception as e:
        conn.close()
        logging.error(f"Error fetching admin logs: {e}")
        return render_template('adminlogs.html', logs=[])

# Yolande - Serve the employee management tab for logged in boss. boss page should have pages only boss can view.
@app.route('/boss')
def boss():
    # Ensure the user has the Boss role.
    if session.get('user_role') != 'Boss':
        return redirect(url_for('main_page'))

    # Get the boss's ID from the session.
    boss_id = session.get('user_id')
    if not boss_id:
        return redirect(url_for('login'))  # Redirect to login if session is invalid.

    try:
        # Connect to the database.
        conn = get_db_connection()

        # Fetch the boss's name.
        boss_name_query = "SELECT Name FROM User WHERE User_ID = ? AND Role = 'Boss'"
        boss_name = conn.execute(boss_name_query, (boss_id,)).fetchone()

        # Fetch employees under the same company as the Boss.
        employees_query = """
            SELECT User_ID, Name, Working
            FROM User
            WHERE Company = (
                SELECT Company
                FROM User
                WHERE User_ID = ? AND Role = 'Boss'
            )
            AND Role = 'Worker'
            AND Working IN ('Yes', 'Disabled')
        """
        employees = conn.execute(employees_query, (boss_id,)).fetchall()

        # Fetch pending requests (Working = "No") for the same company.
        pending_requests_query = """
            SELECT User_ID, Name
            FROM User
            WHERE Company = (
                SELECT Company
                FROM User
                WHERE User_ID = ? AND Role = 'Boss'
            )
            AND Role = 'Worker'
            AND Working = 'No'
        """
        pending_requests = conn.execute(pending_requests_query, (boss_id,)).fetchall()

        conn.close()

        # Render the boss page with data and boss name.
        return render_template(
            'boss.html',
            employees=employees,
            pending_requests=pending_requests,
            name=boss_name['Name'] if boss_name else "Boss"  # Default to Boss if name is not found.
        )

    except sqlite3.Error as e:
        app.logger.error(f"Database error: {e}")
        return jsonify({"error": "Database error"}), 500

##Maria - updates if user is working
@app.route('/update-status', methods=['POST'])
def update_status():
    user_id = request.form.get('user_id')
    working_status = request.form.get('working')
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        ## update working status
        cursor.execute('UPDATE User SET Working = ? WHERE User_ID = ?', (working_status, user_id))
        conn.commit()
        ## get users name for log
        cursor.execute('SELECT Name FROM User WHERE User_ID = ?', (user_id,))
        user = cursor.fetchone()
        user_name = user['Name'] if user else "Unknown User"
        log_user_action(user_id, 'Status Updated', f"User {user_name}'s working status updated to {working_status}.")
        conn.close()
        return jsonify({"status": "success", "message": f"{user_name}'s working status updated to {working_status}."})
    except sqlite3.Error as e:
        app.logger.error(f"Database error: {e}")
        return jsonify({"error": "Failed to update status"}), 500

# Yolande - Boss function to approve user request.
@app.route('/approve-user', methods=['POST'])
def approve_user():
    user_id = request.form.get('user_id')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch the user's name before approval.
        cursor.execute('SELECT Name FROM User WHERE User_ID = ?', (user_id,))
        user = cursor.fetchone()

        if user:
            user_name = user['Name']

            # Approve the user by setting Working to Yes.
            cursor.execute('UPDATE User SET Working = "Yes" WHERE User_ID = ?', (user_id,))
            conn.commit()
            log_user_action(user_id, 'User Approved', f"{user_name} has been approved as a user of the company")
            conn.close()

            return jsonify({"status": "success", "message": f"User {user_name} approved."})
        else:
            conn.close()
            return jsonify({"error": "User not found"}), 404

    except sqlite3.Error as e:
        app.logger.error(f"Database error: {e}")
        return jsonify({"error": "Failed to approve user"}), 500

# Yolande - Boss function to reject user request.
@app.route('/reject-user', methods=['POST'])
def reject_user():
    user_id = request.form.get('user_id')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch the user's name before deletion.
        cursor.execute('SELECT Name FROM User WHERE User_ID = ?', (user_id,))
        user = cursor.fetchone()

        if user:
            user_name = user['Name']

            # Delete the user from the database.
            cursor.execute('DELETE FROM User WHERE User_ID = ?', (user_id,))
            conn.commit()
            conn.close()

            return jsonify({"status": "success", "message": f"User {user_name} rejected and removed."})
        else:
            conn.close()
            return jsonify({"error": "User not found"}), 404

    except sqlite3.Error as e:
        app.logger.error(f"Database error: {e}")
        return jsonify({"error": "Failed to reject user"}), 500

##Maria - display boss logs 
@app.route('/bosslogs', methods=['GET'])
def bosslogs():
    ##only boss
    if session.get('user_role') != 'Boss':
        return redirect(url_for('main_page'))
    user_id = session.get('user_id')
    if not user_id:
        logging.error("User not logged in.")
        return jsonify({"error": "Unauthorized access"}), 401
    conn = get_db_connection()
    try:
        boss_query = 'SELECT Company FROM User WHERE User_ID = ? AND Role = "Boss";'
        boss = conn.execute(boss_query, (user_id,)).fetchone()
        if not boss:
            logging.error(f"User {user_id} is not authorized as Boss.")
            return jsonify({"error": "Unauthorized access"}), 403
        boss_company = boss['Company']
        ## gets logs for users in same company
        logs_query = '''
        SELECT 
            Logs.Timestamp AS Time,
            User.Name AS UserName,
            User.Role AS UserRole,
            Logs.Action_Type AS ActionType,
            Logs.Description AS Description
        FROM Logs
        LEFT JOIN User ON Logs.User_ID = User.User_ID
        WHERE User.Company = ?
        ORDER BY Logs.Timestamp DESC;
        '''
        logs = conn.execute(logs_query, (boss_company,)).fetchall()
        conn.close()
        return render_template('bosslogs.html', logs=logs)
    except Exception as e:
        conn.close()
        logging.error(f"Error fetching boss logs: {e}")
        return jsonify({"error": "Internal server error"}), 500

##Maria - actual logging function
def log_user_action(user_id, action_type, description):
    conn = get_db_connection()
    try:
        query = '''
        INSERT INTO Logs (User_ID, Action_Type, Description)
        VALUES (?, ?, ?);
        '''
        conn.execute(query, (user_id, action_type, description))
        conn.commit()
        logging.info(f"Logged action: {action_type} for User_ID: {user_id}")
    except Exception as e:
        logging.error(f"Failed to log action: {e}")
    finally:
        conn.close()

# Yolande - Logout route.
@app.route('/logout')
def logout():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    try:
        user_id = session.get('user_id')
        if user_id:
            log_user_action(user_id, 'Logout', 'User logged out successfully.')
            session.pop('user_id', None)
            return redirect(url_for('login'))
    except Exception as e:
        # Log any error that happens during the logout process.
        logging.error(f"Error during logout: {e}")
        return redirect(url_for('login'))

# Yolande - Get the API scan status for the asset being currently scanned
@app.route('/get_scan_status', methods=['GET'])
def get_scan_status():
    try:
        user_id = session.get('user_id')  # Get the logged-in user's ID.
        if not user_id:
            return jsonify({"success": False, "message": "User not logged in."}), 401
        
        # Get the current scanning asset for the user.
        asset_id = session.get('current_assets_id')
        if not asset_id:
            return jsonify({"success": False, "message": "No asset currently being scanned."}), 404

        with get_db_connection() as conn:
            result = conn.execute("""
                SELECT Assets_ID, Services, CVE
                FROM API_Status
                WHERE Assets_ID = ?
            """, (asset_id,)).fetchone()

            if not result:
                return jsonify({"success": False, "message": "No scan status found."}), 404

            # Parse the result.
            services_status, cve_status = result[1], result[2]

            # Determine the overall scan status.
            overall_status = "Scan Completed" if services_status == "Completed" and cve_status == "Completed" else \
                             "Scan Failed" if services_status == "Failed" or cve_status == "Failed" else \
                             "Scan Running" if services_status == "Running" or cve_status == "Running" else \
                             "Scan Pending"

            # Return detailed statuses.
            return jsonify({
                "success": True,
                "status": {
                    "Services": services_status,
                    "CVE": cve_status,
                    "Overall": overall_status
                }
            })

    except sqlite3.Error as e:
        app.logger.error(f"Database error: {e}")
        return jsonify({"success": False, "message": "Database error occurred while fetching scan status."}), 500
  
##Maria - validates user input for ip range
@app.route('/store_ip_range', methods=['POST'])
def store_ip_range():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'error': 'User not logged in.'}), 401
    ##get user input 
    ip_range = request.form.get('ip_range')
    if not ip_range:
        return jsonify({'success': False, 'error': 'No IP range provided.'}), 400
    try:
       ## linking to validate docker
        response = requests.post(
            f'{VALIDATEURL}/validate',
            json={'cidr': ip_range}, ##what info to pass
            verify=False, ##verification of certs
            headers={'Content-Type': 'application/json'}
        )
        response.raise_for_status()
        validation_result = response.json()

        if "The IP address range" in validation_result.get("message", "") and "is valid and private" in validation_result["message"]:
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                ## checks if ip range inserting is already inserted into the company 
                query = """
                    SELECT Valid_IP_Range 
                    FROM Maria_Assets 
                    WHERE Valid_IP_Range = ? 
                    AND User_ID IN (
                        SELECT User_ID 
                        FROM User 
                        WHERE Company = (
                            SELECT Company 
                            FROM User 
                            WHERE User_ID = ?
                        )
                    );
                """
                cursor.execute(query, (ip_range, user_id))
                existing_ip = cursor.fetchone()
                ## if ip range already in db for company, reject
                if existing_ip:
                    conn.close()
                    return jsonify({
                        'success': False,
                        'error': 'The IP range has already been stored for your company. Please proceed to assets page if you want to scan it.'
                    }), 400
                ## inserting ip range
                insert_query = """
                    INSERT INTO Maria_Assets (Valid_IP_Range, User_ID)
                    VALUES (?, ?);
                """
                cursor.execute(insert_query, (ip_range, user_id))
                conn.commit()
                conn.close()
                logging.info(f"Stored IP range: {ip_range} in db.")
                log_user_action(user_id, 'IP Validation', f"Successfully stored IP range {ip_range} in the database.")
                return jsonify({'success': True, 'message': 'IP range validated and stored successfully.'}), 200
            except sqlite3.Error as e:
                logging.error(f"Failed to store IP range in the database: {e}")
                return jsonify({'success': False, 'error': f'Failed to store IP range.'}), 500
        else:
            return jsonify({'success': False, 'error': validation_result.get('message', 'Invalid IP range.')}), 400
    except requests.exceptions.RequestException as e:
        logging.error(f"Validation service error: {e}")
        return jsonify({'success': False, 'error': f'Validation error.'}), 500

##Maria - gets validate ip range for dropdown
@app.route('/get_validated_ip_ranges', methods=['GET'])
def get_validated_ip_ranges():
    if 'user_id' not in session:
        return jsonify({"success": False, "error": "User not authenticated."}), 401
    user_id = session.get('user_id')
    user_role = session.get('user_role')
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            user_company = cursor.execute("""
                SELECT Company 
                FROM User 
                WHERE User_ID = ?
            """, (user_id,)).fetchone()
            if not user_company or not user_company['Company']:
                return jsonify({"success": False, "error": "User's company not found."}), 400
            ##get ip range of user's company
            rows = cursor.execute("""
                SELECT DISTINCT ma.Valid_IP_Range
                FROM Maria_Assets ma
                JOIN User u ON ma.User_ID = u.User_ID
                WHERE u.Company = ?
            """, (user_company['Company'],)).fetchall()
            ip_ranges = [row['Valid_IP_Range'] for row in rows]
            logging.debug(f'ip_ranges: {ip_ranges}')
            return jsonify({"success": True, "data": ip_ranges})
    except sqlite3.Error as e:
        app.logger.error(f"Database error: {e}")
        return jsonify({"success": False, "error": "Database error."}), 500

##Maria - detects active hosts
@app.route('/checkassets', methods=['GET'])
def checkassets():
    if 'user_id' not in session:
        return jsonify({"success": False, "error": "User not authenticated."}), 401
    user_id = session.get('user_id')  
    ##gets ip range provided
    ip_range = request.args.get('valid_ip')
    if not ip_range:
        return jsonify({"success": False, "error": "No IP range provided."}), 400
    try:
        with get_db_connection() as conn:
            row = conn.execute(""" 
                SELECT Assets_ID, Valid_IP_Range 
                FROM Maria_Assets 
                WHERE Valid_IP_Range = ? 
            """, (ip_range,)).fetchone()
            if not row:
                return jsonify({"success": False, "error": "IP range not found."}), 404
            assets_id = row["Assets_ID"]
            ##connects to validate docker for asset scan
            response = requests.get(
                f"{VALIDATEURL}/checkassets",
                verify=False,
                params={"valid_ip": ip_range}
            )
            response.raise_for_status()
            active_assets = response.json().get("message", "")
            ##update db with active assets
            conn.execute(""" 
                UPDATE Maria_Assets
                SET Active_Assets = ?
                WHERE Valid_IP_Range = ?;
            """, (active_assets, ip_range))
            ##prevents duplicates by checking via assets_id
            existing_row = conn.execute(""" 
                SELECT Status_ID FROM API_Status WHERE Assets_ID = ? 
            """, (assets_id,)).fetchone()
            if existing_row:
                ##update existing row
                conn.execute(""" 
                    UPDATE API_Status
                    SET Discovery = 'Completed', Services = 'Not Running', CVE = 'Not Running'
                    WHERE Assets_ID = ?;
                """, (assets_id,))
            else:
                ##inserts new row
                conn.execute(""" 
                    INSERT INTO API_Status (Discovery, Services, CVE, Assets_ID)
                    VALUES ('Completed', 'Not Running', 'Not Running', ?);
                """, (assets_id,))
            conn.commit()
            log_user_action(user_id, 'Asset Scan', f"Completed scan for IP range {ip_range}, found active assets: {active_assets}.")
            return jsonify({"success": True, "message": "Asset scan completed successfully."}), 200
    except sqlite3.Error as e:
        app.logger.error(f"Database error: {e}")
        return jsonify({"success": False, "error": "Database error."}), 500
    except requests.RequestException as e:
        app.logger.error(f"Request to FastAPI failed: {e}")
        return jsonify({"success": False, "error": "Failed to connect to FastAPI service."}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({"success": False, "error": "Unexpected error."}), 500

# Madeline - Gets IP ranges that user can scan for services (by company)
@app.route('/services_get_ip_ranges', methods=['GET'])
def services_get_ip_ranges():
    # Check if the session contains user_id == for inactivity / verify is logged in 
    if 'user_id' not in session:
        return jsonify({'error': 'User not logged in'}), 401

    user_id = session['user_id']
    
    try:
        conn = get_db_connection()
        
        # Fetch the user's company from the User table
        user_data = conn.execute(
            'SELECT Company FROM User WHERE User_ID = ?',
            (user_id,)
        ).fetchone()

        # Just in case, should not have this err - but may come up in testing if things dont tally 
        if not user_data:
            return jsonify({'error': 'User not tied to a company'}), 404

        company_name = user_data['Company']

        # Fetch IP ranges (which may have been entered by other users) for the user's company
        rows = conn.execute("""
            SELECT ma.Valid_IP_Range, ma.Active_Assets
            FROM Maria_Assets ma
            JOIN User u ON ma.User_ID = u.User_ID
            WHERE u.Company = ?
        """, (company_name,)).fetchall()

        # Extract IP ranges into a list
        #    Should only get ip ranges that have active assets / ips 
        ip_ranges = [row['Valid_IP_Range'] for row in rows if row['Active_Assets']]
        logging.info(f'ip_ranges: {ip_ranges}')
        
        return jsonify({'success': True, 'ip_ranges': ip_ranges})

    except Exception as e:
        # Log the error for debugging
        print(f"Error in /services_get_ip_ranges: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

# Madeline - Get IPs for dropdown for the entering of credentials (ssh key)
@app.route('/credential_get_ip_addresses', methods=['GET'])
def credential_get_ip_addresses():
    if 'user_id' not in session:
        return jsonify({"success": False, "error": "User not authenticated."}), 401

    user_id = session.get('user_id')

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            # Get the company of the logged-in user
            user_company = cursor.execute("""
                SELECT Company 
                FROM User 
                WHERE User_ID = ?
            """, (user_id,)).fetchone()

            if not user_company or not user_company['Company']:
                return jsonify({"success": False, "error": "User's company not found."}), 400
            
            user_company = user_company['Company']
            
            # Fetch IPs of the active assets for the user's company 
            #    applies for admin also since they only allowed to scan their own ip ranges
            rows = cursor.execute("""
                SELECT DISTINCT ma.Active_Assets
                FROM Maria_Assets ma
                JOIN User u ON ma.User_ID = u.User_ID
                WHERE u.Company = ?
            """, (user_company,)).fetchall()

            ips = []
            for row in rows:
                assets = row['Active_Assets']
                
                # If can get assets == have assets stored for that company 
                if assets and assets.strip() and assets != 'No Active Assets':
                    # Since active_assets stored "ip1, ip2" - need to split to get ind ips
                    ips.extend([ip.strip() for ip in assets.split(', ')])

            logging.debug(f'IPs for {user_company}\'s company: {ips}')
            
            return jsonify({"success": True, "data": ips})
        
    except sqlite3.Error as e:
        app.logger.error(f"Database error: {e}")
        return jsonify({"success": False, "error": "Database error.", "details": str(e)}), 500

# Madeline - Check if ssh key entered by user is of valid format
async def validate_ssh_key(ssh_key):
    try:
        # Parse the key using asyncssh  - to see if valid 
        asyncssh.import_private_key(ssh_key)
        return True
    except asyncssh.KeyImportError:
        return False

# Madeline - Encrypt SSH private key using AES-256-CBC
def encrypt_private_key(ssh_key):
    # Generate random IV
    iv = os.urandom(IV_SIZE)  
    
    # Generate random encryption key
    encryption_key = os.urandom(ENCRYPTION_KEY_SIZE)  
    
    # Pad the SSH key to make it a multiple of AES block size 
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(ssh_key.encode()) + padder.finalize()
    
    # Encrypt the SSH key
    cipher = Cipher(algorithms.AES(encryption_key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    
    # Return the IV + encryption key + encrypted data, all base64 encoded - shorter 
    return base64.b64encode(iv + encryption_key + encrypted_data).decode('utf-8')

# Madeline - Decrypt stored private key 
def decrypt_private_key(encrypted_data):
    try:
        # Decode the cred (stored into db as base64 so shorter)
        encrypted_data = base64.b64decode(encrypted_data.encode('utf-8'))
        
        # Extract IV (16 bytes), encryption key (32 bytes), and encrypted key
        iv = encrypted_data[:IV_SIZE]
        encryption_key = encrypted_data[IV_SIZE:IV_SIZE + ENCRYPTION_KEY_SIZE]
        to_be_decrypted = encrypted_data[IV_SIZE + ENCRYPTION_KEY_SIZE:]
        
        # Decrypt the SSH key
        cipher = Cipher(algorithms.AES(encryption_key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(to_be_decrypted) + decryptor.finalize()
        
        # Unpad the decrypted key
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        original_data = unpadder.update(decrypted_data) + unpadder.finalize()
        
        return original_data.decode('utf-8')
    
    except (base64.binascii.Error, ValueError) as e:
        # Handle incorrect format or Base64 decoding errors
        logging.error(f"Error: Invalid format or Base64 decoding failed - {e}")
        return None
    
    except Exception as e:
        # Catch other unexpected errors
        logging.error(f"Error: Decryption failed - {e}")
        return None

# Madeline - Save entered SSH key into db 
@app.route('/save_credentials', methods=['POST'])
def save_credentials():
    # Make sure user_id is there == if logged in / not inactive 
    if 'user_id' not in session:
        return jsonify({"success": False, "error": "User not authenticated."}), 401
    
    user_id = session.get('user_id')
    user_role = session.get('user_role')  

    ip_address = request.form.get('ipAddressDropdown')
    credential = request.form.get('inputCredential').strip().strip('\n')

    # Unlikely but in case of when testing that it's bypassed 
    if not ip_address or not credential:
        return jsonify({'success': False, 'message': 'Missing required fields'})

    # Validate SSH private key asynchronously
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    key_is_valid = loop.run_until_complete(validate_ssh_key(credential))

    # the funct returns a bool -> T (valid), F (invalid)
    if not key_is_valid:
        return jsonify({'success': False, 'message': 'Invalid SSH private key format'})

    conn = get_db_connection()
    
    try:
        logging.info('running encryption')
        # Encrypt the private key b4 storing into db  
        combined_iv_pwd_cred = encrypt_private_key(credential)
        
        # Insert the credential into db, match it to respective ip
        conn.execute(''' 
            INSERT INTO Madeline_Credentials (User_ID, IP_Address, Credential) 
            VALUES (?, ?, ?)
        ''', (user_id, ip_address, combined_iv_pwd_cred))
        
        conn.commit()
        
        return jsonify({'success': True})

    except sqlite3.Error as e:
        app.logger.error(f"Database error: {e}")
        return jsonify({'success': False, 'message': 'An error occurred while saving the credential'})

    finally:
        conn.close()

# Madeline - get services info & store into db 
@app.route('/get_services_version', methods=['POST'])
def get_services_version_internal():
    ip_range = request.form.get('ip_range')
    user_id = session.get('user_id') 
    user_role = session.get('user_role')
    
    conn = None
    try:
        conn = get_db_connection()
        
        # Get the company of logged-in user
        user_company = conn.execute("""
            SELECT Company 
            FROM User 
            WHERE User_ID = ?
        """, (user_id,)).fetchone()

        if not user_company or not user_company['Company']:
            return jsonify({"success": False, "error": "User's company not found."}), 400
        
        user_company = user_company['Company']
        logging.info(f'company: {user_company}')
        
        # Would get latest Assets - check thru all users from same company 
        #    applies to admin also since they should only be scanning the assets of admins ('Overall' company)
        query = """
            SELECT ma.Assets_ID, ma.Active_Assets
            FROM Maria_Assets ma
            JOIN User u ON ma.User_ID = u.User_ID
            WHERE ma.Valid_IP_Range = ? 
            AND u.Company = ?
            ORDER BY Assets_ID DESC
            LIMIT 1;
        """
        result = conn.execute(query, (ip_range, user_company)).fetchone()            
            
        # If can retrieve == have info 
        if result:
            # Make sure can be accessed as needed (in dict form)
            result = dict(result)
            logging.info(f'get ips from maria db: {result}')
            
            # Getting the IPs that are up
            ip_range = result["Active_Assets"].strip('\n')
            
            # To know which scan it is
            asset_id = result["Assets_ID"]
            
            # Store asset_id in session
            session['current_assets_id'] = asset_id  
        
        # More for edge case. IRL case: interception / testing
        else:
            return jsonify({"success": False, "message": "No matching record found in the database."})
        
        # Clear prev record of services from that asset_id
        #    a, don't overlap serv that found for same ip
        #    b, services IP address that != active would still be shown elsewise
        query = """
            DELETE FROM Madeline_Services WHERE Assets_ID = ?;
        """
        result = conn.execute(query, (asset_id,))
        conn.commit()
        
        # If there are no up IPs, then no need to do scanning, just mark scan complete
        if ip_range == '':
            query = """
                UPDATE API_Status
                SET Services = 'Completed', CVE = 'Completed'
                WHERE Assets_ID = ?
            """
            result = conn.execute(query, (asset_id,))
            conn.commit()
            
            return jsonify({"success": True, "message": "No active assets found."})
        
        # Store that the services discovery portion is running
        else:
            query = """
                UPDATE API_Status
                SET Services = 'Running', CVE = 'Not Running'
                WHERE Assets_ID = ?
            """
            result = conn.execute(query, (asset_id,))
            conn.commit()
        
        # Fetch credentials stored by other users in same comany as current user
        #    Sort by desc id so get latest credential stored for each ip 
        query = """
        SELECT 
            mc.IP_Address, mc.Credential
        FROM Madeline_Credentials mc
        WHERE mc.Credential_ID IN (
            SELECT MAX(mc2.Credential_ID)
            FROM Madeline_Credentials mc2
            WHERE mc2.IP_Address = mc.IP_Address
            GROUP BY mc2.IP_Address
        )
        AND mc.User_ID IN (
            SELECT u.User_ID
            FROM User u
            WHERE u.Company = ?
        )
        ORDER BY mc.Credential_ID DESC
        """
        result = conn.execute(query, (user_company,)).fetchall()
        
        credentials = {}
        
        # If can retrieve == have pkeys stored
        if result:
            for row in result:
                ip = row['IP_Address']
                
                # Check if this ip got creds stored b4
                #    if have, then append 
                #    else, new entry 
                if ip in credentials:
                    logging.info(f'running decryption for {ip} key')
                    # Decrypt the private key before using as cred for SSH
                    decrypted = decrypt_private_key(row['Credential'].strip('\n'))
                    
                    # Only if != None means decrypt successfully 
                    if decrypted:
                        credentials[ip].append(decrypted)
                    
                else:
                    logging.info(f'running decryption for {ip} key')
                    # Decrypt the private key before using as cred for SSH
                    decrypted = decrypt_private_key(row['Credential'].strip('\n'))
                    
                    # Only if != None means decrypt successfully 
                    if decrypted:
                        credentials[ip] = [decrypted]
        
        # Send the data to FastAPI
        response = requests.post(
            "https://fastapi:8000/get_serv_vers", 
            json={"ip_range": ip_range, 'possible_credentials': credentials},
            verify=False
        )
        
        # Log the full response to understand its structure
        logging.info('Response status: %s', response.status_code)
        logging.info('Response JSON: %s', response.json())
        
        if response.status_code == 200:
            # Extracting the result (ips & their serv info) from the JSON response
            # It only contains dict of results 
            services_info = dict(response.json())
            
            # Edge case I suppose, but catch in case of issues
            if services_info == {}:
                error_msg = 'Something wrong with services.py'
                logging.error(error_msg)
                return jsonify({"success": False, "message": error_msg})
            
            # Full serv info -> also includes pid 
            for ip, full_service_info in services_info.items():
                
                for pid, serv_info in full_service_info.items():
                    # pid would be 'error' if 
                    #    a, ssh credentials are wrong 
                    #    b, no services running == cannot ssh in 
                    if pid == 'error':
                        # More to log & verify that can / cannot ssh in
                        logging.info(f'Unable to ssh into {ip}')
                        
                        # Save the serv info as ''
                        conn.execute("""
                            INSERT INTO Madeline_Services (Assets_ID, User_ID, IP_Address, Services, Version, Ports, Package_Name, Process_Name)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                        """, (
                            asset_id, user_id, ip, '', '', '', '', ''                                
                        ))
                    
                    # If there's a pid == got a service, store in db
                    else:
                        conn.execute("""
                            INSERT INTO Madeline_Services (Assets_ID, User_ID, IP_Address, Services, Version, Ports, Package_Name, Process_Name)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                        """, (
                            asset_id, user_id, ip, 
                            serv_info.get('service_name'), serv_info.get('version'), 
                            serv_info.get('ports'), serv_info.get('package_name'), 
                            serv_info.get('process_name')
                        ))
                        
                    # Commit the changes
                    conn.commit()
                
                # Need to change status to completed  
                else:
                    query = """
                        UPDATE API_Status
                        SET Services = 'Completed'
                        WHERE Assets_ID = ?
                    """
                    # Execute the query with params
                    result = conn.execute(query, (asset_id,))
                    conn.commit()
                    
            logging.info('Successfully got services info + stored in db')
            # If can get resp from script == success, then call trigger_cve_lookup function 
            trigger_cve_lookup(asset_id, user_id)
        
        # If script cannot run / have errors, fail services + cve 
        else:
            query = """
                UPDATE API_Status
                SET Services = 'Failed', CVE = 'Failed'
                WHERE Assets_ID = ?
            """
            # Execute the query with params
            result = conn.execute(query, (asset_id,))
            conn.commit()
            return jsonify({"success": False, "message": "Error message1"})
        
        return jsonify({"success": True, "message": "Services have been stored."})

    except Exception as e:
        # If an error occurs + connected to db, we still need to update status as failed
        if conn:
            query = """
                UPDATE API_Status
                SET Services = 'Failed', CVE = 'Failed'
                WHERE Assets_ID = ?
            """
            # Execute the query with params
            result = conn.execute(query, (asset_id,))
            conn.commit()
        
        return jsonify({"success": False, "message": f"An error occurred: {e}"})

    # will always be run aft try / except so will close db connection 
    finally:
        if conn:
            conn.close()

# Yee Xiang - Fetches CVE data from the external API with retries. It sends a POST request to the FASTAPI server, receives the response, and returns the data in a structured format.
def fetch_cve_data(version, version_name):
    retries = 3  # Set the number of retries if the request fails
    for attempt in range(retries):
        try:
            # Send a POST request to the FastAPI server
            response = requests.post(
                FASTAPI_URL,
                json={"version_name": version_name, "version_number": version},
                verify=False,  # Disable SSL verification (for testing purposes)
                headers={"Content-Type": "application/json"},
                timeout=60  # Set the timeout to 60 seconds
            )
            logging.debug(f"Request sent to {FASTAPI_URL}: version={version}, name={version_name}")
            
            # If the response is successful (status code 200), process the data
            if response.status_code == 200:
                data = response.json()
                logging.debug(f"Raw response: {data}")
                return data if isinstance(data, list) else []
            else:
                logging.error(f"API error for version {version}, name {version_name}: {response.text}")
        except requests.RequestException as e:
            logging.error(f"Attempt {attempt + 1} failed for version {version}: {e}")
    
    # Return a default CVE data when all attempts to fetch data fail
    logging.warning(f"Failed to fetch CVE data after {retries} attempts for version={version}, name={version_name}")
    return [{"Description": "No CVE data found for the given parameters.", "CVSS Score": 0, "Severity": "Unknown", "References": [], "Publish Date": "N/A"}]

# Yee Xiang - Cleans the version string by removing prefixes and extracting the major, minor, and patch numbers. It ensures that the version is in the correct format (major.minor.patch).
def clean_version(version):
    """
    Cleans the version string by removing prefixes (e.g., "5:") and extracting the major, minor, and patch numbers.
    Handles various versioning formats such as package metadata or suffixes.
    """
    if not version or version.strip() == "":  # Check if version is empty
        return "N/A"  # Return "N/A" if version is empty or whitespace

    # Remove prefix like "5:", "1:", or other package name prefixes before the version
    if ":" in version:
        version = version.split(":", 1)[1]  # Remove everything before and including the colon

    # Remove any suffix after the version number, such as "-1~debian", "-bookworm", "-beta", "+20130313144759"
    version = re.sub(r'[-~+].*$', '', version)

    # Match the cleaned version (major.minor.patch) format
    match = re.match(r'^(\d+)(?:\.(\d+))?(?:\.(\d+))?', version)
    if match:
        major = match.group(1)
        minor = match.group(2) if match.group(2) else "0"  # Default minor to 0 if missing
        patch = match.group(3) if match.group(3) else "0"  # Default patch to 0 if missing
        return f"{major}.{minor}.{patch}"

    # If no match is found, return "N/A" to avoid incorrect processing
    return "N/A"


# Yee Xiang - Handles the CVE lookup process for the provided asset and user ID. It supports both predefined scan data (from a test file) and real CVE data retrieval via API.
def trigger_cve_lookup(asset_id, user_id):
    try:
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row  # Allows dictionary-like access to DB rows
        logging.info(f"Triggering CVE lookup for Asset ID: {asset_id}, User ID: {user_id}")

        # Set API_Status to 'Running' before processing
        conn.execute("""
            UPDATE API_Status
            SET CVE = 'Running'
            WHERE Assets_ID = ?;
        """, (asset_id,))
        conn.commit()

        # Check if redirect_to_test flag is set to True to use predefined scan data (e.g., 192.json)
        if redirect_to_test:
            try:
                logging.info(f"Current directory: {os.getcwd()}")
                if os.path.exists('test_192.json'):
                    with open('test_192.json', 'r') as file:
                        scan_data = json.load(file)
                    logging.info("Serving predefined data from 192.json.")
                else:
                    logging.info('File not found in OS. Returning error.')
                    return jsonify({"error": "test_192.json file not found!"}), 500
            except Exception as e:
                logging.error(f'Error loading file: {e}, {traceback.format_exc()}')
                return jsonify({"error": "Error loading the test file!"}), 500

            try:
                # Insert predefined scan data into the database
                for item in scan_data:
                    conn.execute("""
                        INSERT INTO Yee_Xiang_CVE (Cve_Number, CVSS_Score, Severity, Reference_Link, Publish_Date, User_ID, Assets_ID, Services_ID)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                    """, (
                        item.get("CVE ID", "N/A"),
                        item.get("CVSS Score", 0),
                        item.get("Severity", "Unknown"),
                        ",".join(item.get("References", [])),
                        item.get("Publish Date", "N/A"),
                        user_id,
                        item.get("Assets_ID", 1),  # Correct JSON key for Assets_ID
                        item.get("Service ID", 1)   # Correct JSON key for Service ID
                    ))

                conn.commit()
                logging.info("Predefined scan data inserted into the database.")

                # Update API_Status to 'Completed' after inserting predefined scan data
                conn.execute("""
                    UPDATE API_Status
                    SET CVE = 'Completed'
                    WHERE Assets_ID = ?;
                """, (asset_id,))
                conn.commit()

                return jsonify(scan_data)  # Return the content of 192.json instead of performing the real lookup

            except FileNotFoundError:
                logging.error("test_192.json file not found!")
                return jsonify({"error": "test_192.json file not found!"}), 500

        else:
            # Proceed with real CVE scan
            logging.info("Proceeding with normal CVE scan (not using predefined JSON).")
            services = conn.execute("""
                SELECT Services_ID, Version, Services
                FROM Madeline_Services
                WHERE Assets_ID = ?;
            """, (asset_id,)).fetchall()

            if not services:
                logging.warning(f"No services found for Asset ID: {asset_id}. Using default CVE data.")
                services = [{'Services_ID': None, 'Version': "N/A", 'Services': "N/A"}]

            for service in services:
                services_id = service['Services_ID']
                version = service['Version'] if service['Version'] != "" else "N/A"
                version_name = service['Services'] if service['Services'] != "" else "N/A"
                cleaned_version = clean_version(version)
                logging.info(f"Looking up CVEs for Service ID: {services_id}, Version: {cleaned_version}, Name: {version_name}")

                cve_data = fetch_cve_data(cleaned_version, version_name) if version_name and cleaned_version != "N/A" else [{
                    "CVE ID": "N/A",
                    "CVSS Score": 0,
                    "Severity": "Unknown",
                    "References": [],
                    "Publish Date": "N/A"
                }]

                cve_data_sorted = sorted(
                    cve_data,
                    key=lambda x: datetime.strptime(x['Publish Date'], '%Y-%m-%dT%H:%M:%S.%f') if x['Publish Date'] != 'N/A' else datetime.min,
                    reverse=True
                )

                for cve in cve_data_sorted:
                    conn.execute("""
                        INSERT INTO Yee_Xiang_CVE (Services_ID, Assets_ID, Cve_Number, CVSS_Score, Severity, Reference_Link, User_ID, Publish_Date)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                    """, (
                        services_id,
                        asset_id,
                        cve.get("CVE ID", "N/A"),
                        cve.get("CVSS Score", 0),
                        cve.get("Severity", "Unknown"),
                        ",".join(cve.get("References", [])),
                        user_id,
                        cve.get("Publish Date", "N/A")
                    ))

            conn.commit()

            # Mark CVE lookup as Completed
            conn.execute("""
                UPDATE API_Status
                SET CVE = 'Completed'
                WHERE Assets_ID = ?;
            """, (asset_id,))
            conn.commit()

            logging.info(f"CVE lookup completed for Asset ID: {asset_id}")

    except sqlite3.Error as e:
        logging.error(f"Database error during CVE lookup: {e}")
        conn.execute("""
            UPDATE API_Status
            SET CVE = 'Failed'
            WHERE Assets_ID = ?;
        """, (asset_id,))
        conn.commit()
    finally:
        conn.close()

if __name__ == '__main__':
    # Set the secret key (secure method using a random value or environment variable)
    app.secret_key = secrets.token_urlsafe(16)  # Generates a random 16-byte URL-safe key
    app.run(debug=True, host='0.0.0.0', port=3000)
