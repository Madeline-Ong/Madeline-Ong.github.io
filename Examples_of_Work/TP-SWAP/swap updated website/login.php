<!-- AUTHOR: MADELINE ONG YING XUAN -->
<!-- LAST UPDATED: 19/01/2024 -->
<!-- SUMMARY: THIS FILE TAKES IN ID AND PASSWORD ENTERED BY EMPLOYEE -->


<!-- Setting that this is a html file and the language is English -->
<!DOCTYPE html>
<!-- Session is started/resumed so that can check for error message stored as session variable -->
<?php session_start();?>
<html lang="en">
<head>
	<!-- Meta data sets that the page uses UTF8 encoding, max width of content is same as width of device's screen -->
    <!-- Page is displayed is at its normal size, without zooming in -->
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login Form</title>
    <!-- Styling for the login page -->
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .login-container {
            width: 300px;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            background-color: rgba(0, 0, 0, 0.7); 
            color: white;
        }

        h2 {
            text-align: center;
            margin-bottom: 20px;
            color: #fff; 
        }

        form {
            padding: 20px;
            border-radius: 8px;
        }
        input[type="text"],
        input[type="password"],
        button[type="submit"] {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
            color: #000;
        }
        button[type="submit"] {
            background-color: #007bff;
            color: #fff;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        button[type="submit"]:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
	<!-- Container for login, also since the css is tied to the name -->
    <div class="login-container">
    	<?php
    	//Includes code from shared.php (in this case using decrypt_data function)
    	include 'shared.php';
    	//Retrieve and decrypt the error message and previous login form values.
    	//Then output error message and have previous login form values:
    	if (isset($_SESSION['msg'])) {
    	    $msg = decrypt_data($_SESSION['msg']);
    	    //Outputs the error message as red text
    	    echo "<p style='color: red;'>{$msg}</p>"; 
    	    $decrypted_query = decrypt_data($_SESSION['form_values']);
    	    //Parse query string into variables and store in array
    	    parse_str($decrypted_query, $data);
    	}
    	?>
    	<!-- Login form. Get the value for employee id if user has tried to login and was redirected here -->
        <form action="login_do.php" method="post">
            <h2>Login</h2>
            <input type="text" name="entered_id" placeholder="Employee ID" required
value="<?php echo isset($data['entered_id']) ? htmlspecialchars($data['entered_id']) : ''; ?>">
            <br>
			<input type="password" name="entered_password" placeholder="Password" required>
			<br><br>
            <button type="submit" name="submit">Login</button>
        </form>
    </div>
</body>
</html>