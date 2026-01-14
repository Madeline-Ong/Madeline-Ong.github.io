<!-- AUTHOR: JOVAN CHUA RUI CHENG -->
<!-- LAST UPDATED: 18/01/2024 -->
<!-- SUMMARY: THIS FILE IS THE FORM TO GET INPUT VALUES OF OTP FROM USERS -->
<!DOCTYPE html>
<html lang="en">
<?php
//Resume the sessions
session_start();

//To include shared.php and check_session.php
include 'check_session.php';
include 'shared.php';

//Set an array of allowed referers
$allowed_referer=array('personal_information.php','otp.php');

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
	<title>Update User Information</title>
	
	<!-- To use CSS from shared_css_form.php -->
	<?php include 'shared_css_form.php'; ?>

</head>
<body>
	<!-- To use navbar.php -->
	<?php include "navbar.php"; ?>
	
	<!-- This form is to help us send our inputted value to otp_check.php -->
	<form method='post' action='otp_check.php'>
		<h1>OTP</h1>
		
		<?php
    	//Checks if error message is set in session, and if so display the error message and unset it
    	if (isset($_SESSION['msg'])) {
    	    $msg = decrypt_data($_SESSION['msg']);
    	    echo "<p style='color: red;'>{$msg}</p>";
    	    unset($_SESSION['msg']);
    	}
    	?>
    	   	
    	<label for='otp'>Please enter the 6-digit OTP sent to your email: </label>
    	<br>
    	
    	<!-- Input to take in value for OTP -->
    	<input type='text' id='otp' name='entered_otp'>
    	<br><br>
    	
    	<!-- Button to resend OTP -->
    	<button id="otp_resend" onclick="resend_otp()">Resend OTP</button>
    	
    	<script>
    		//Sets variable delay as 10000 milliseconds, which is 10 seconds
    		var delay = 10000;
    		
    		//Sets variable resend_button as the button to resend OTP
    		var resend_button = document.getElementById('otp_resend');
    		
    		//Disable resend_button when the page is loaded
    		window.onload = function () {
                resend_button.disabled = true;
            };
            
            //Set resend_button to be not disabled after 10 seconds
    		setTimeout(function(){
    			resend_button.disabled = false;
    		}, delay);
    		
    		//Function to resend OTP
    		function resend_otp(){
    			//Set the resend_button to be disabled, helps avoid sending multiple request
    			resend_button.disabled = true;
                
                //Create and append a hidden form to the document to redirect to otp_generate.php using post method
    			var form = document.createElement('form');
    			form.style.display = 'none';
    			form.action = 'otp_generate.php';
    			form.method = 'post';
    			document.body.appendChild(form);
    			
    			// Append a hidden input field with name 'submit_button' and value 'true'
                var input = document.createElement('input');
                input.type = 'hidden';
                input.name = 'submit_button';
                input.value = 'true';
                form.appendChild(input);
    			
    			try {
                    //Submit the form
    				form.submit();
                } catch (error) {
                    console.error('From not submitting:', error);
                }
            }
        </script>
        
        <!-- Button to submit OTP -->
        <button type='submit' name="submit">Submit</button>
        
	</form>
</body>
</html>
