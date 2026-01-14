<?php
include 'shared.php';
session_start();

$user_id = $_SESSION['user_id'];
$employee_id = $_SESSION['employee_id'];

$con = mysqli_connect("localhost", "root", $database_password, "tp_amc_hr"); // connect to database
if (! $con) {
    die('Could not connect: ' . mysqli_connect_errno()); // return error is connect fail
}

//reset acct status to 'logged out' from 'locked'
$reset_acct_status = $con->query('UPDATE user_accounts
SET account_status = DEFAULT
WHERE employee_id = ' . $employee_id);

//need to reset failed attempts to 0 else acct would just get locked again 
//when user tries to login as login_do checks failed attempts
$reset_pwd_failed_attempts = $con->query('UPDATE user_accounts
SET password_failed_attempts = 0
WHERE employee_id = ' . $employee_id);

//reset acct pwd to the default one (acct is locked)
$reset_acct_pwd = $con->query('UPDATE user_accounts
SET password = DEFAULT
WHERE employee_id = ' . $employee_id);

//log that pwd was reset
$post_log = $con->prepare('INSERT INTO activity_log (action, time) VALUES (?, ?)');
$action = "{$user_id} reset the account status and password of {$employee_id}.";
$post_log->bind_param('ss', $action, $time);
$post_log->execute();
$post_log->close();

$con->close();

header('Location: /swap updated website/list_employees.php');
?>