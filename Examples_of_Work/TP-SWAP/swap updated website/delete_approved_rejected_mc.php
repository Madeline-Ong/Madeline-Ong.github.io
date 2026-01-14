<?php
include 'shared.php';
session_start();

$user_id = $_SESSION['user_id'];

$con = mysqli_connect("localhost", "root", $database_password, "tp_amc_hr"); // connect to database
if (! $con) {
    die('Could not connect: ' . mysqli_connect_errno()); // return error is connect fail
}

//delete approved or rejecte mc applications from db
$del_mc = $con->query('DELETE FROM mc_application
WHERE status = "approved" OR status = "rejected"');
if ($del_mc){
    //log that approved and rejected mc were cleared
    $post_log = $con->prepare('INSERT INTO activity_log (action, time) VALUES (?, ?)');
    $action = $user_id . ' cleared the approved and rejected MC applications.';
    $post_log->bind_param('ss', $action, $time);
    $post_log->execute();
    $post_log->close();
    header('Location: /swap updated website/list_mc_application.php');
}
$con->close();

?>