<?php
session_start();
include 'shared.php';
$redirect='Location: /swap updated website/leave_application.php';
if (!isset($_POST['submit'])){
    header($redirect);
    exit();
}
$user_id = $_SESSION['user_id'];

$start_date = $_POST['start_date'];
$end_date = $_POST['end_date'];
$reason = $_POST['reason'];


//check date funct: if year is this year or next
$start_date = date_check($start_date);
$end_date = date_check($end_date);
if (!preg_match($check_reason, $reason)){
    $_SESSION['msg'] = encrypt_data('Reason should only include letters and numbers, no full stop or commas.');
    $_SESSION['form_values'] = encrypt_data(http_build_query($_POST)); // Convert form values to query string
    header($redirect);
    exit();
}
//check that end date is aft start date
//could be same day thats why its only <
if ($start_date && $end_date) {
    if ($end_date < $start_date){
        $_SESSION['msg'] = encrypt_data('End date should be later than start date.');
        $_SESSION['form_values'] = encrypt_data(http_build_query($_POST)); // Convert form values to query string
        header($redirect);
        exit();
    }
} else {
    $_SESSION['msg'] = encrypt_data('Dates should be from today onwards and is up to next year.');
    $_SESSION['form_values'] = encrypt_data(http_build_query($_POST)); // Convert form values to query string
    header($redirect);
    exit();
}

//get num of days of leave, how many days is 2nd date ahead
$leave_days = $start_date->diff($end_date);
$leave_days = $leave_days->format('%a') + 1;  //one more day added to include the day of
$start_date = $start_date->format('Y-m-d');
$end_date = $end_date->format('Y-m-d');

//connect to db
$con = mysqli_connect("localhost","root",$database_password,"tp_amc_hr"); //connect to database
if (!$con){
    die('Could not connect: ' . mysqli_connect_errno()); //return error is connect fail
}

//query to find out num of leave days taken
$check_leave = $con->query('SELECT leave_days_taken FROM employee_information
WHERE employee_id='.$user_id);
$leave_days_taken = ($check_leave->fetch_row())[0];
$check_leave->close();

$leave_days_allowed = 15; //for all employees, only 15 days allowed

//check if the employee has enough leave days
if (($leave_days_allowed - $leave_days_taken) < $leave_days){
    $_SESSION['msg'] = encrypt_data('You do not have enough leave days to apply.');
    $_SESSION['form_values'] = encrypt_data(http_build_query($_POST)); // Convert form values to query string
    header($redirect);
    exit();
} else {
    //update database of new leave application
    $apply_leave = $con->prepare('INSERT INTO leave_application(employee_id,
reason, start_date, end_date) VALUES (?,?,?,?)');
    $apply_leave->bind_param('isss', $user_id, $reason, $start_date, $end_date);
    $apply_leave->execute();
    $apply_leave->close();
      
    //post log
    $post_log = $con->prepare('INSERT INTO activity_log (action, time) VALUES (?, ?)');
    $action = $user_id . ' applied for leave.';
    $post_log->bind_param('ss', $action, $time);
    $post_log->execute();
    $post_log->close();
    unset($_SESSION['msg']);
    unset($_SESSION['form_values']);
    header('Location: /swap updated website/leave_view.php');
}

?>