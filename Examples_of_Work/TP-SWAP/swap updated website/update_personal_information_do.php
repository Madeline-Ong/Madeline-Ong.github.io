<?php
include "shared.php";
session_start();
if (!isset($_POST['submit'])){
    header('Location: /swap updated website/update_personal_information.php');
    exit();
}
$user_id = $_SESSION['user_id'];
$contact = $_POST['contact'];
$email = $_POST['email'];
$bank_account = $_POST['bank_account'];

//check the personal info entered
if (!preg_match($check_contact, $contact)){
    $msg = "Contact number should only contain 8 numbers.";
} elseif (!filter_var($email, FILTER_VALIDATE_EMAIL)){
    $msg = "Email format is invalid.";
} elseif(!preg_match($check_email,$email)){
    //Validate the email domain
    $msg = "Please only use gmails.";
} elseif (!preg_match($check_bank_account, $bank_account)){
    $msg = "Bank account should only have numbers and -.";
}else {
    $con = mysqli_connect("localhost","root",$database_password,"tp_amc_hr"); //connect to database
    if (!$con){
        die('Could not connect: ' . mysqli_connect_errno()); //return error is connect fail
    }
    
    //updating info in db
    $update = $con->prepare('UPDATE employee_information SET contact = ?,
    email = ?, bank_account = ? WHERE employee_id = ?');
    $contact = encrypt_data($contact);
    $email = encrypt_data($email);
    $bank_account = encrypt_data($bank_account);
    $update->bind_param('sssi', $contact, $email, $bank_account, $user_id);
    
    if ($update->execute()){
        $msg = "successful";
        //log that user info changed
        $post_log = $con->prepare('INSERT INTO activity_log (action, time) VALUES (?, ?)');
        $action = 'Personal information of ' . $user_id . ' was updated.';
        $post_log->bind_param('ss', $action, $time);
        $post_log->execute();
        $post_log->close();
        
        
        header("Location: /swap updated website/personal_information.php");
        exit();
    } else {
        $msg = "Contact HR. Error in updating personal information.";
    }
}
$_SESSION['msg'] = encrypt_data($msg);
$_SESSION['form_values'] = encrypt_data(http_build_query($_POST)); // Convert form values to query string
header("Location: /swap updated website/update_personal_information.php");



?>
