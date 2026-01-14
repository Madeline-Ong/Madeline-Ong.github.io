<!-- AUTHOR: JOVAN CHUA RUI CHENG -->
<!-- LAST UPDATED: 18/01/2024 -->
<!-- SUMMARY: THIS FILE TO TAKE IN VALIDATE AND PARSE IN INPUTS FROM CHANGE PASSWORD -->

<?php
//Resume the sessions
session_start();

//To include shared.php
include "shared.php";

//Check if the page was called/redirected from a button from change_password.php,
//else redirect to personal_information.php
if (!isset($_POST['submit'])){
    header("Location: /swap updated website/personal_information.php");
    exit();
}

//Get user employee ID from sessions
$user_id = $_SESSION['user_id'];

//Set variabls for the passwords
$current_password = hash('sha256', $_POST['current_password']);
$check_new_password = $_POST['new_password'];
$new_password = hash('sha256', $_POST['new_password']);
$confirm_new_password = hash('sha256',$_POST['confirm_new_password']);

//Connect to database and check if the connection fails, return an error
$con = mysqli_connect("localhost","root",$database_password,"tp_amc_hr");
if(!$con){
    die('Could not connect: ' . mysqli_connect_errno());
}

//Get the stored current password
$get_information = $con->prepare('SELECT password FROM user_accounts WHERE employee_id=?');
$get_information->bind_param('i', $user_id);

//Set the variable for the stored password and decrypt it
if($get_information->execute()){
    $result = $get_information->get_result();
    $information = $result->fetch_assoc();
    $stored_password = decrypt_data($information['password']);
} else {
    //If $get_information was not executed successfully, prompt error
    $msg = "Please contact IT for assistance.";
    $con->close();
    $_SESSION['msg'] = encrypt_data($msg);
    header("Location: /swap updated website/change_password.php");
    exit();
}


if($current_password != $stored_password){
    //Checks if the current password input is the same as the stored password
    $msg = "Current password is not correct. Please try again.";
} elseif ($current_password == $new_password){
    //Checks if the new password is the same as the stored password
    $msg = "New password should not be same as old password. Please try again.";
} elseif (!preg_match($check_password, $check_new_password)){
    //Checks if the new password matches the predefined password policy that we have
    $msg = 'Your new password does not fulfil the password policy: Minimum length of
    8 characters. At least one uppercase, one lowercase letter. At least one digit.
    At least one special character';
} elseif ($new_password != $confirm_new_password){
    //Check if the new password matfches the confirm new password
    $msg = "New password does not match the confirm password. Please try again.";
} else {
    //If pass checks, hash and encrypt new password and store it in database
    $new_password = encrypt_data($new_password);
    $update_password = $con->prepare('UPDATE user_accounts SET password = ? WHERE employee_id = ?');
    $update_password->bind_param('si', $new_password, $user_id);
    if ($update_password->execute()){
        //Log that user has changed password and close database connections
        $post_log = $con->prepare('INSERT INTO activity_log (action, time) VALUES (?, ?)');
        $action = "{$user_id}'s password was changed";
        $post_log->bind_param('ss', $action, $time);
        $post_log->execute();
        $post_log->close();
        $get_information->close();
        $update_password->close();
        $con->close();
        //If there is error message in the session unset it
        if(isset($_SESSION['msg'])){
            unset($_SESSION['msg']);
        }
        header("Location: /swap updated website/personal_information.php");
        exit();
    } else {
        $msg = "Contact HR. Error updating password.";
        $update_password->close();
    }
}

//Close database connections and set error to be in sessions, and redirect back to change_password.php
$get_information->close();
$con->close();
$_SESSION['msg'] = encrypt_data($msg);
header("Location: /swap updated website/change_password.php");
exit();
