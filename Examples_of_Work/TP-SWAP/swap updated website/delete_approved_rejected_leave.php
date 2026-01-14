<?php
include 'shared.php';
session_start();

$user_id = $_SESSION['user_id'];

$con = mysqli_connect("localhost", "root", $database_password, "tp_amc_hr"); // connect to database
if (! $con) {
    die('Could not connect: ' . mysqli_connect_errno()); // return error is connect fail
}

//delete approved or rejecte leave applications from db 
$del_leave = $con->query('DELETE FROM leave_application
WHERE status = "approved" OR status = "rejected"');
if ($del_leave){
    //log that approved and rejected leaves were cleared
    $post_log = $con->prepare('INSERT INTO activity_log (action, time) VALUES (?, ?)');
    $action = $user_id . ' cleared the approved and rejected leave applications.';
    $post_log->bind_param('ss', $action, $time);
    $post_log->execute();
    $post_log->close();
    header('Location: /swap updated website/list_leave_application.php');
}
$con->close();

?>