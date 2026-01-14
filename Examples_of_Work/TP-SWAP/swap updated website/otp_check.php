<!-- AUTHOR: JOVAN CHUA RUI CHENG -->
<!-- LAST UPDATED: 18/01/2024 -->
<!-- SUMMARY: THIS FILE TO VALIDATE OTP -->

<?php
//Resume the sessions
session_start();

//To include shared.php and check_session.php
include "shared.php";
include "check_session.php";

//Check if the page was called/redirected from a button from otp.php, else redirect to personal_information.php
if (!isset($_POST['submit'])){
    header("Location: /swap updated website/personal_information.php");
    exit();
}

//Set time_expiry to be 600 seconds
$time_expiry = 10 * 60;

//Use time_expiry variable to check if OTP has expired after 10 minutes by calling the otp_expiry set in session
if (time() - $_SESSION['otp_expiry'] > $time_expiry) {
    $_SESSION['msg'] = encrypt_data("This OTP has expired. Please request for a new one.");
    header("Location: /swap updated website/otp.php");
    exit();
}

//Get OTP from session and hash entered_otp
$otp = $_SESSION['otp'];
$entered_otp = hash('sha256', $_POST['entered_otp']);

//Check if entered otp is same as generated otp, if not same redirect to otp.php
//and prompt error, else unset session and redirect to change_password.php and set a session 'change_password'
if ($entered_otp != $otp){
    $_SESSION['msg'] = encrypt_data("Incorrect OTP, please try again.");
    header("Location: /swap updated website/otp.php");
    exit();
}
else {
    //If there is error message in the session unset it
    if(isset($_SESSION['msg'])){
        unset($_SESSION['msg']);
    }
    unset($_SESSION['otp']);
    header("Location: /swap updated website/change_password.php");
    exit();
}
