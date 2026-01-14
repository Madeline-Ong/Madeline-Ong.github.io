<!-- AUTHOR: JOVAN CHUA RUI CHENG -->
<!-- LAST UPDATED: 18/01/2024 -->
<!-- SUMMARY: THIS FILE IS TO GENERATE OTP -->

<?php
//Resume the sessions
session_start();

//To include shared.php
include "shared.php";

//Check if the page was called/redirected from a button from personal_information.php, else redirect it back
if (!isset($_POST['submit_button'])){
    header("Location: /swap updated website/personal_information.php");
    exit();
}

//Get user employee id from sessions
$user_id = $_SESSION['user_id'];

//Generate random OTP
$otp = rand(100000,999999);

//Connect to database and check if the connection fails, return an error
$con = mysqli_connect("localhost", "root", $database_password, "tp_amc_hr");
if (!$con) {
    die('Could not connect: ' . mysqli_connect_errno());
}

//Get the email and name of employee from database
$get_info = $con->prepare('SELECT name,email FROM employee_information WHERE employee_id=?');
$get_info->bind_param('i', $user_id);
if(!$get_info->execute()){
    echo "Error: Failed to get ID from database. Please contact IT for assistance.";
}

//Associate and decrypt the fetched information with variables and close the connection
$result = $get_info->get_result();
$info = $result->fetch_assoc();
$name = $info['name'];
$email = decrypt_data($info['email']);
$get_info->close();
$con->close();

//Get the files needed from specified directory (include path)
set_include_path('C:/xampp/php/pear/PHPMailer');
require 'src/Exception.php';
require 'src/PHPMailer.php';
require 'src/SMTP.php';

//Import PHPMailer classes into the global namespace
use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

//create instance of PHPMailer class
$mail = new PHPMailer;

//Configure SMTP settings for the mailer
$mail->isSMTP();
$mail->Host = "smtp.gmail.com";
$mail->Port = 587;
$mail->SMTPSecure = 'tls';
$mail->SMTPAuth = true;
$mail->Username = "tpamc87@gmail.com";
$mail->Password = "emonckafmgrefhuf";

//Set the details of the email
$mail->setFrom("tpamc87@gmail.com");
$mail->addAddress($email);
$mail->Subject = 'One-Time Password (OTP) for Verification';
$mail->IsHTML(true);
$mail->Body = 'Dear ' . $name . ',<br><br>' .
    'Do not share this OTP with anyone. You have requested a One-Time Password
(OTP) to reset your password.<br><br>' .
'Your email OTP is: ' . $otp . '<br><br>' .
'Please enter this code on the verification page to proceed. If you did not
request this OTP or have any concerns, please contact our support team
immediately.<br><br>
Best regards,<br>
Temasek Polytechnic Advanced Manufacturing Centre</p>';

//Hash OTP and store as a session
$_SESSION['otp'] = hash('sha256', $otp);

//Send mail and check for failure, if no error set a session to clock in the OTP generated
//time to be used for further checking and proceed
if(!$mail->send()){
   echo "Error: OTP Failed to send";
} else {
    $_SESSION['otp_expiry'] = time();
    header("Location: /swap updated website/otp.php");
    exit();
}
