<?php
session_start();
include 'shared.php';
$redirect = 'Location: /swap updated website/mc_application.php';
if (!isset($_POST['submit'])){
    header($redirect);
    exit();
}

$user_id = $_SESSION['user_id'];

$start_date = $_POST['start_date'];
$end_date = $_POST['end_date'];

//check date funct: if year is this year or next
$start_date = date_check($start_date);
$end_date = date_check($end_date);

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

//get num of days of mc, how many days is 2nd date ahead
$mc_days = $start_date->diff($end_date);
$mc_days = $mc_days->format('%a') + 1;  //one more day added to include the day of
$start_date = $start_date->format('Y-m-d');
$end_date = $end_date->format('Y-m-d');


//check for mc file type
$file_type = $_FILES['mc']['type']; //returns the mimetype
if(isset($_FILES['mc'])){
    $file_type = $_FILES['mc']['type']; //returns the mimetype
    $allowed = array('image/png', 'image/jpg', 'image/jpeg');
    if(!in_array($file_type, $allowed)) {
        $_SESSION['msg'] = encrypt_data('The file attached is not supported.');
        $_SESSION['form_values'] = encrypt_data(http_build_query($_POST)); // Convert form values to query string
        header($redirect);
        exit();
    }
}
else {
    $_SESSION['msg'] = encrypt_data('There is no file attached.');
    $_SESSION['form_values'] = encrypt_data(http_build_query($_POST)); // Convert form values to query string
    header($redirect);
    exit();
}
//only assign to variable if mc is proper file type
$mc = file_get_contents($_FILES["mc"]["tmp_name"]);



//connect to db
$con = mysqli_connect("localhost","root",$database_password,"tp_amc_hr"); //connect to database
if (!$con){
    die('Could not connect: ' . mysqli_connect_errno()); //return error is connect fail
}

//query to find out num of mc days taken
$check_mc = $con->query('SELECT mc_days_taken FROM employee_information
WHERE employee_id='.$user_id);
$mc_days_taken = ($check_mc->fetch_row())[0];
$check_mc->close();

$mc_days_allowed = 15; //for all employees, only 15 days allowed

//check if the employee has enough mc days
if (($mc_days_allowed - $mc_days_taken) < $mc_days){
    $_SESSION['msg'] = encrypt_data('You do not have enough MC days to apply.');
    $_SESSION['form_values'] = encrypt_data(http_build_query($_POST)); // Convert form values to query string
    header($redirect);
    exit();
} else {
    //update database of new mc application
    $apply_mc = $con->prepare('INSERT INTO mc_application(employee_id,
mc_picture, start_date, end_date) VALUES (?,?,?,?)');
    $apply_mc->bind_param('isss', $user_id, $mc, $start_date, $end_date);
    $apply_mc->execute();
    $apply_mc->close();
    
    //post log
    $post_log = $con->prepare('INSERT INTO activity_log (action, time) VALUES (?, ?)');
    $action = $user_id . ' applied for MC.';
    $post_log->bind_param('ss', $action, $time);
    $post_log->execute();
    $post_log->close();
    
    header('Location: /swap updated website/mc_view.php');
}

?>
