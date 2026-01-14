<?php
session_start();
include 'shared.php';

$user_id = $_SESSION['user_id'];
$mc_id = $_SESSION['mc_id'];

$con = mysqli_connect("localhost", "root", $database_password, "tp_amc_hr"); // connect to database
if (! $con) {
    die('Could not connect: ' . mysqli_connect_errno()); // return error is connect fail
}
$get_mc_info = $con->query("SELECT employee_id,start_date,end_date FROM mc_application WHERE mc_id={$mc_id}");
$mc_info = $get_mc_info->fetch_assoc();
$employee_id = $mc_info['employee_id'];
//update num of mc days taken for employee
$get_mc_days_taken = $con->query("SELECT mc_days_taken FROM employee_information
WHERE employee_id = {$employee_id}");
$mc_days_taken = ($get_mc_days_taken->fetch_assoc())['mc_days_taken'];
//calc mc days taken & update in db
$start_date = new DateTime($mc_info['start_date']);
$end_date = new DateTime($mc_info['end_date']);
$mc_days = $start_date->diff($end_date);
$mc_days = $mc_days->format('%a') + 1;
$mc_days_taken += $mc_days;

//if enough mc days then can approve
if ($mc_days_taken > 15) {
    $msg = encrypt_data("The employee does not have enough MC days for this MC. This application will be rejected.");
    //update status of mc, rejected
    $reject_mc = $con->query("UPDATE mc_application
    SET status = 'rejected'
    WHERE mc_id = {$mc_id}");
    header("Location: /swap updated website/list_mc_application.php?msg={$msg}");
}
else {
    //update status of mc, approved & update days in db
    $approve_mc = $con->query("UPDATE mc_application
SET status = 'approved'
WHERE mc_id = {$mc_id}");
    $mc_days_update = $con->query("UPDATE employee_information
SET mc_days_taken={$mc_days_taken}
WHERE employee_id = {$employee_id}");
    
    //log that mc was approved
    $post_log = $con->prepare('INSERT INTO activity_log (action, time) VALUES (?, ?)');
    $action = $user_id . ' approved the MC application ' . $mc_id;
    $post_log->bind_param('ss', $action, $time);
    $post_log->execute();
    $post_log->close();
    
    //redirect back to list of mc applications
    header('Location: /swap updated website/list_mc_application.php');
}
$con->close();
unset($_SESSION['mc_id']);

?>