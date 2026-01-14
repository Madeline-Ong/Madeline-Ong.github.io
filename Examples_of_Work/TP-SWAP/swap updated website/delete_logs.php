<?php
include 'shared.php';
session_start();

$user_id = $_SESSION['user_id'];

$con = mysqli_connect("localhost", "root", $database_password, "tp_amc_hr"); // connect to database
if (! $con) {
    die('Could not connect: ' . mysqli_connect_errno()); // return error is connect fail
}

$del_all_log = $con->query('DELETE FROM activity_log');
if ($del_all_log){
    //log that logs was deleted
    $post_log = $con->prepare('INSERT INTO activity_log (action, time) VALUES (?, ?)');
    $action = $user_id . ' cleared the logs.';
    $post_log->bind_param('ss', $action, $time);
    $post_log->execute();
    $post_log->close();
    
    header('Location: /swap updated website/list_logs.php');
}
$con->close();