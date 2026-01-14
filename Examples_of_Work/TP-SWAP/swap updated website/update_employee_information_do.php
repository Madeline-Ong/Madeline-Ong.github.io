<?php
include "shared.php";
session_start();
$user_level = $_SESSION['user_level'];
check_lvl($user_level, 2);
$user_id = $_SESSION['user_id'];
$employee_id=$_SESSION['employee_id'];
$salary=$_POST['salary'];
$department=strtoupper($_POST['department']);
$list_department=array('HR','IT','FINANCE');

$con = mysqli_connect("localhost","root",$database_password,"tp_amc_hr"); //connect to database
if (!$con){
    die('Could not connect: ' . mysqli_connect_errno()); //return error is connect fail
}

//convert salary vari to str type so can use str funct to input validate
if(preg_match($check_salary, $salary)==False){
    $_SESSION['msg'] = encrypt_data("Salary should only contain whole numbers.");
    $_SESSION['form_values'] = encrypt_data(http_build_query($_POST)); // Convert form values to query string
    header("Location: /swap updated website/update_employee_information.php");
    exit();
}

if(preg_match($check_department, $department)==False || in_array($department, $list_department)==False){
    $_SESSION['msg'] = encrypt_data("No such department.");
    $_SESSION['form_values'] = encrypt_data(http_build_query($_POST)); // Convert form values to query string
    header("Location: /swap updated website/update_employee_information.php");
    exit();
}
//updating employee info
$update = $con->prepare('UPDATE employee_information SET salary = ?, department = ? WHERE employee_id = ?');
$salary = encrypt_data($salary);
$update->bind_param("ssi", $salary, $department, $employee_id);
$update->execute();

//log that employee info changed
$post_log = $con->prepare('INSERT INTO activity_log (action, time) VALUES (?, ?)');
$action = $user_id . ' updated employee information of ' . $employee_id;
$post_log->bind_param('ss', $action, $time);
$post_log->execute();
$post_log->close();



if($department == "HR"){
    $update_user = $con->prepare('UPDATE user_accounts SET user_account_level = 2 WHERE employee_id = ?');
} else {
    $update_user = $con->prepare('UPDATE user_accounts SET user_account_level = 1 WHERE employee_id = ?');
}

$update_user->bind_param("i", $employee_id);
$update_user->execute();

header('Location: /swap updated website/view_employee_information.php');
exit();
?>