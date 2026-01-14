<?php
session_start();
include 'shared.php';

$user_id = $_SESSION['user_id'];
$leave_id = $_SESSION['leave_id'];

$con = mysqli_connect("localhost", "root", $database_password, "tp_amc_hr"); // connect to database
if (! $con) {
    die('Could not connect: ' . mysqli_connect_errno()); // return error is connect fail
}

$get_leave_info = $con->query("SELECT employee_id,start_date,end_date FROM leave_application WHERE leave_id={$leave_id}");
$leave_info = $get_leave_info->fetch_assoc();
$employee_id = $leave_info['employee_id'];
//update num of leave days taken for employee
$get_leave_days_taken = $con->query("SELECT leave_days_taken FROM employee_information
WHERE employee_id = {$employee_id}");
$leave_days_taken = ($get_leave_days_taken->fetch_assoc())['leave_days_taken'];
//calc leave days taken & update in db
$start_date = new DateTime($leave_info['start_date']);
$end_date = new DateTime($leave_info['end_date']);
$leave_days = $start_date->diff($end_date);
$leave_days = $leave_days->format('%a') + 1;
$leave_days_taken += $leave_days;

//if enough leave days then can approve
if ($leave_days_taken > 15) {
    $_SESSION['msg'] = encrypt_data("The employee does not have enough leave days for this leave. This application will be rejected.");
    //update status of leave, rejected
    $reject_leave = $con->query("UPDATE leave_application
    SET status = 'rejected'
    WHERE leave_id = {$leave_id}");
    header("Location: /swap updated website/list_leave_application.php");
} 
else {
    //update status of leave, approved & update days in db
    $approve_leave = $con->query("UPDATE leave_application
SET status = 'approved'
WHERE leave_id = {$leave_id}");
    $leave_days_update = $con->query("UPDATE employee_information
SET leave_days_taken={$leave_days_taken}
WHERE employee_id = {$employee_id}");

    //log that leave was approved
    $post_log = $con->prepare('INSERT INTO activity_log (action, time) VALUES (?, ?)');
    $action = $user_id . ' approved the leave application ' . $leave_id;
    $post_log->bind_param('ss', $action, $time);
    $post_log->execute();
    $post_log->close();
    
    //redirect back to list of leave applications
    header('Location: /swap updated website/list_leave_application.php');
}

$con->close();
unset($_SESSION['leave_id']);
?>