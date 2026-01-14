<!-- AUTHOR: JOVAN CHUA RUI CHENG -->
<!-- LAST UPDATED: 18/01/2024 -->
<!-- SUMMARY: THIS FILE TO TAKE IN INPUTS TO HELP CHANGE PASSWORD -->

<!DOCTYPE html>
<html lang="en">
<?php
//Resume the sessions
session_start();

//To include shared.php and check_session.php
include 'check_session.php';
include 'shared.php';

//Set an array of allowed referers
$allowed_referer=array('change_password.php','otp.php');

//Find out and set what is the refer in the HTTP request
$refer_page = isset($_SERVER['HTTP_REFERER']) ? $_SERVER['HTTP_REFERER'] : '';

//Check if the referer is from array of allowed referer, else redirect back to personal_information.php
if(!in_array(basename($refer_page),$allowed_referer)){
    header('Location: /swap updated website/personal_information.php');
    exit();
}
?>
<head>
    <meta charset="UTF-8">
    <title>Change Password</title>
    
    <!-- To use CSS from shared_css_form.php -->
	<?php include 'shared_css_form.php'; ?>
</head>

<body>
	<!-- To use navbar.php -->
	<?php include "navbar.php";	?>
	
	<!-- Form to take in input for changing password -->
	<form action="change_password_do.php" method="post">
    	<h2>Change password</h2>
    	
    	<?php
    	//Checks if error message is set in session, and if so display the error message and unset it
        if (isset($_SESSION['msg'])) {
            $msg = decrypt_data($_SESSION['msg']);
            echo "<p style='color: red;'>{$msg}</p>";
            unset($_SESSION['msg']);
        }
        ?>
        
        <!-- Input for current password -->
		<label for="current_password">Current Password:</label>
		<input type="password" id="current_password" name="current_password" required>
		<br><br>
		
		<!-- Input for new password -->
		<label for="new_password">New Password:</label>
		<input type="password" id="new_password" name="new_password" required>
		<br><br>
		
		<!-- Input for confirm new password -->
		<label for="confirm_new_password">Confirm New Password:</label>
		<input type="password" id="confirm_new_password" name="confirm_new_password" required>
		<br><br><br>
		
		<!-- Button to submit -->
		<button type="submit" name="submit">Submit</button>
	</form>
</body>
</html>
