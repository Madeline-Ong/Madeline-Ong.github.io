<?php
include 'shared.php';
session_start();

$user_id = $_SESSION['user_id'];
$mc_id = $_SESSION['mc_id'];

$con = mysqli_connect("localhost", "root", $database_password, "tp_amc_hr"); // connect to database
if (! $con) {
    die('Could not connect: ' . mysqli_connect_errno()); // return error is connect fail
}

//update status of mc, rejected
$reject_mc = $con->query('UPDATE mc_application
SET status = "rejected"
WHERE mc_id = ' . $mc_id);
if ($reject_mc){
    //log that mc was rejected
    $post_log = $con->prepare('INSERT INTO activity_log (action, time) VALUES (?, ?)');
    $action = $user_id . ' rejected the MC application of id ' . $mc_id;
    $post_log->bind_param('ss', $action, $time);
    $post_log->execute();
    $post_log->close();
    
    //redirect back to list of mc applications
    header('Location: /swap updated website/list_mc_application.php');    
}
$con->close();
unset($_SESSION['mc_id']);

?>