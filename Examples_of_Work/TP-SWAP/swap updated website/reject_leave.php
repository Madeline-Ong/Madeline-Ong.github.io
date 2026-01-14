<?php
include 'shared.php';
session_start();

$user_id = $_SESSION['user_id'];
$leave_id = $_SESSION['leave_id'];

$con = mysqli_connect("localhost", "root", $database_password, "tp_amc_hr"); // connect to database
if (! $con) {
    die('Could not connect: ' . mysqli_connect_errno()); // return error is connect fail
}

//update status of leave, rejected
$reject_leave = $con->query('UPDATE leave_application
SET status = "rejected"
WHERE leave_id = ' . $leave_id);
if ($reject_leave){
    //log that leave was rejected
    $post_log = $con->prepare('INSERT INTO activity_log (action, time) VALUES (?, ?)');
    $action = $user_id . ' rejected the leave application of id ' . $leave_id;
    $post_log->bind_param('ss', $action, $time);
    $post_log->execute();
    $post_log->close();
    
    //redirect back to list of leave applications
    header('Location: /swap updated website/list_leave_application.php');
}
$con->close();
unset($_SESSION['leave_id']);

?>