<?php
//AUTHOR: MADELINE ONG YING XUAN
//LAST UPDATED: 19/01/2024
//SUMMARY: THIS FILE DELETES THE EMPLOYEE FROM THE DATABASE AND LOGS THE DELETION

//Session is resumed so can retrieve the session variables to be used:
session_start();

//Code is included from shared.php ($time variable is intialised there):
include 'shared.php';

//Retrieving session variables user_id and employee_id:
$user_id = $_SESSION['user_id'];
$employee_id = $_SESSION['employee_id'];

//To connect to database:
$con = mysqli_connect("localhost", "root", $database_password, "tp_amc_hr");

//If the connection fails, return an error:
if (!$con) {
    die('Could not connect: ' . mysqli_connect_errno());
}

//Preparing SQL query to delete the employee from database:
//(database is set to cascade so other tables will be affected by foreign key, employee_id being deleted)
$del_employee = $con->prepare('DELETE FROM employee_information WHERE employee_id = ?');

//Binding the parameter (employee_id, which is an integer) to the prepared SQL query:
$del_employee->bind_param('i', $employee_id);

//If employee is deleted successfully, log that employee was deleted then redirect to list of employees:
if ($del_employee->execute()){
    //Preparing SQL query to log that an employee has been deleted from the database:
    $post_log = $con->prepare('INSERT INTO activity_log (action, time) VALUES (?, ?)');
    
    //Logging which employee was the one to delete this employee
    $action = "{$user_id} deleted employee {$employee_id}.";
    
    //Binding the parameters (action and time, which are considered text) to the prepared SQL query:
    $post_log->bind_param('ss', $action, $time);
    
    //Executing the prepared SQL query:
    $post_log->execute();
    
    //Closing prepared SQL query to free up resources:
    $post_log->close();
    
    header('Location: /swap updated website/list_employees.php');
}
//Connection to database is closed to free up resources:
$con->close();
