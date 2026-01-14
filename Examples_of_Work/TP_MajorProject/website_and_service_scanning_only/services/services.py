import requests
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import json
import logging
import os
import re
import traceback
import asyncio, asyncssh

logging.basicConfig(level=logging.INFO) 
logging.captureWarnings(True)

# If need to redirect to test json results == True
# To run the scans and all, set False
redirect_to_test = True

# JSON file w results
TEST_VM_FILE = "./vm_result.json"

# Initialize FastAPI app
app = FastAPI()

# Define the input params (& their type) using Pydantic
class GetIPRange(BaseModel):
    ip_range: str
    possible_credentials: dict

# Middleware to handle redirection - to return prepared res || run scan 
@app.middleware("http")
async def redirect_middleware(request: Request, call_next):
    global redirect_to_test
    
    # Unlikely that would be called using != post but in case of interception
    if request.method == "POST":
        try:
            # Wait for the req json
            body = await request.json()
            
            # If ip_range isnt specified (which shouldn't happen), put nth
            ip_range = body.get("ip_range", "")
        except Exception:
            ip_range = ""
    else:
        ip_range = ""
    
    logging.info(f'ip_range check: {ip_range}')
    
    # So if redirect is set to T, will get json test res
    #    If redir == F, then will run normal scan 
    if redirect_to_test:
        # Check if input is the iprange for vms 
        if "192.168.56." in ip_range:
            try:
                logging.info(f'getting {TEST_VM_FILE} json file for middleware')
                with open(TEST_VM_FILE, "r") as f:
                    logging.info(f'getting json content')
                    return JSONResponse(content=json.load(f))
            except FileNotFoundError:
                logging.error(f"File not found: {TEST_VM_FILE}")
                raise HTTPException(status_code=500, detail=f"{TEST_VM_FILE} not found")
        
        # If ip range is not predefined then dh json, so will cont to run normal scan 
        else:
            logging.error(f"No json file for {ip_range}")
            
    return await call_next(request)

class SSHConnectionManager:
    def __init__(self):
        # Store active SSH connections
        self.connections = {}

    # To create the conn to ip & store that conn 
    async def create_connection(self, ip, private_key=None):
        try:
            # Using private key to ssh
            conn = await asyncssh.connect(ip, client_keys=private_key, known_hosts=None, connect_timeout=5)
            logging.info(f'Connection established with {ip}')
            return conn
        
        # If cannot private key authentication, print error 
        except (asyncssh.KeyImportError, asyncssh.PermissionDenied) as e:
            logging.error(f'Private key authentication failed for {ip}: {e}')
        
        # Need to catch both since the connect_timeout (asyncio.wait_for function) would raise general asyncio.TimeoutError 
        #    asyncssh.TimeoutError is more for if ssh connection takes a while 
        except (asyncssh.TimeoutError, asyncio.TimeoutError) as e:
            logging.error(f'Connection timed out with {ip}: {e}')
            return None
        
        # Catch all other errors
        except Exception as e:
            logging.error(f'Failed to connect to {ip}: {e}, {traceback.format_exc()}')
            return None
    
    # sftp transfer bash script file, chmod so can run 
    async def sftp_transfer_file(self, conn, local_file, remote_file):
        async with conn.start_sftp_client() as sftp:
            # Upload the file
            await sftp.put(local_file, remote_file)
            logging.info('File uploaded')

            # Change its perms - can be executed 
            result = await conn.run(f'chmod 750 {remote_file}')
            logging.info(f'File permissions changed: {result.stdout}')
    
    # Run commands - specified below in the main funct (get_serv_vers)
    async def run_command(self, conn, command, password=None):
        if conn:
            try:
                # If cmd need pwd, when it's called, will pass in the pwd
                #    Cmd can be run w/o password would not have pwd passed in & can run
                result = await conn.run(f'echo {password} | {command}', check=True)
                return result.stdout
            
            # If cmd cannot run, show the err 
            except asyncssh.ProcessError as exc:
                logging.error(f'Command with status {exc.exit_status}: {exc.stderr}')
                return f'Error: {exc.stderr}'

    # Remove bash script file
    async def sftp_remove_file(self, conn, remote_file):
        # Start SFTP client session over existing SSH conn
        async with conn.start_sftp_client() as sftp:
            await sftp.remove(remote_file)
            logging.info('File removed')
            
    # Close sftp conn
    async def close_connection(self, conn):
        if conn:
            # Close SSH conn
            conn.close()
            
            # Wait for conn to fully close
            await conn.wait_closed()
            logging.info('Connection closed')

# Checks through the service scan info & remove those w/o proc || version || pkg name
def sanitised_result(services):
    cleaned_services = {}
    for pid, service_info in services.items():
        # Check if the service has info
        # These 2 are more likely to have since when run ss (gets running serv, which uses ports)
        #  + will only get proc w proc name 
        ports = service_info.get('ports')
        proc_name = service_info.get('process_name')
        
        # These may not have values, which is why its being cleaned 
        # Checking all for redundancy but only need to check for vers / serv name
        pkg_name = service_info.get('package_name', None)
        serv_vers = service_info.get('version', None)
        serv_name = service_info.get('service_name', None)
        
        # If pkg_name & serv_vers & serv_name can be found, then store 
        if pkg_name and serv_vers and serv_name:
            # Cleaning the version num
            #    If version has num:text, remove the num: part, text onwards is version
            match = re.match(r'^\d+:(.*)', serv_vers)
            if match:
                serv_vers = match.group(1)
            
            # Store cleaned serv info
            cleaned_services[pid] = {
                'service_name': serv_name,
                'version': serv_vers,
                'ports': ports,
                'package_name': pkg_name,
                'process_name': proc_name
            }
        
    return cleaned_services

# Main funct to call other sub functions 
@app.post("/get_serv_vers")
async def get_serv_vers(request: GetIPRange):
    # Since active_assets is saved in the db as "ip1, ip2", so split by ", "
    #    make sure format is the same, even if only have 1 asset will be converted to list format
    ip_range = request.ip_range.split(", ") if ", " in request.ip_range else [request.ip_range]
    
    # Gets the creds saved for user's company from the req 
    possible_credentials = request.possible_credentials
    
    local_file = "get_services_version.sh"
    remote_path = "./get_services_version.sh"
    key_path = './pkey'
    
    all_ip_res = {}
    manager = SSHConnectionManager()
    for ip in ip_range:
        # Check if under creds saved contains the up ip
        ip_creds = possible_credentials.get(ip, None)
        
        # IF have then run as per normal 
        if ip_creds:
            
            # Trying to ssh w each possible key tied to that ip addr 
            for creds in ip_creds:
                
                # Store pkey location as format 
                pkey_location = [key_path]
                
                # Open the pkey file (should be able to write to it)
                with open(key_path, 'w') as file:
                    
                    # Write retrieved private key to the file 
                    file.write(creds)
                    
                # Change perms of file - not allow tamper 
                os.chmod(key_path, 0o600)
                
                # Try to ssh w the private key 
                conn = await manager.create_connection(ip, private_key=pkey_location)
                if not conn:
                    
                    # Store err msg so know that couldnt ssh 
                    all_ip_res[ip] = {'error': 'SSH Connection failed'}
                    
                    # Since cannot ssh, dn to cont w rest of code 
                    continue
                
                # Transfer the script
                await manager.sftp_transfer_file(conn, local_file, remote_path)

                # Run the script 
                output = await manager.run_command(conn, f"bash {remote_path}")
                
                # Load the output as json
                output = json.loads(output)
                logging.debug(f'output: {output}')
                
                # Cleaning up: Remove the script 
                await manager.sftp_remove_file(conn, remote_path)
                
                # Once done, close the ssh connection 
                await manager.close_connection(conn)
                
                # Store results 
                all_ip_res[ip] = sanitised_result(output)
        
        # If dh, then can't ssh so dont run coe, just store error 
        else:
            all_ip_res[ip] = {'error': 'No credential for this IP Address'}
    
    # Delete the private key aft use
    if os.path.exists(key_path):
        os.remove(key_path)

    # Check the final result 
    logging.info(f'all_ip_res: {all_ip_res}')
    return all_ip_res
