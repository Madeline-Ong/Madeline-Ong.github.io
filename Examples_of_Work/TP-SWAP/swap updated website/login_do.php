<?php
//AUTHOR: MADELINE ONG YING XUAN
//LAST UPDATED: 19/01/2024
//SUMMARY: THIS FILE CHECKS THE ENTERED ID AND PASSWORD. IF CORRECT, DIRECT TO HOME.
//IF NOT, REDIRECT TO LOGIN PAGE AND OUTPUT THE ERROR.

//Session is resumed so can retrieve the session variables to be used:
session_start();

//Encrypt_data funct, regex of id, $time variable is intialised in shared.php
include 'shared.php';

$redirect_location = "Location: /swap updated website/login.php";

//To check if login button (button name=submit) was pressed.
//If not pressed, user should not be able to access or run the login process
if (!isset($_POST['submit'])){
    echo $redirect_error;
    exit();
} else {
    //To get the entered employee id from posted login form:
    $entered_id = $_POST['entered_id'];
    //To get the entered password from posted login form:
    //Password is hashed so can be compared. (password in database is hashed then encrypted)
    $entered_password = hash('sha256', $_POST['entered_password']);
}

//To check if entered id is a valid id, which is an integer:
if (!preg_match($check_id, $entered_id)){
    //Setting session variable msg which stores the error message (that id is invalid)
    //Which would be used in login.php to display the error message:
    $_SESSION['msg'] = encrypt_data("Please enter a valid ID.");
    //Form values are converted to query string, then encrypted.
    //Then stored as session variable so that entered id can be displayed in login.php:
    $_SESSION['form_values'] = encrypt_data(http_build_query($_POST));
    header($redirect_location);
    exit();
}

//To connect to database:
$con = mysqli_connect("localhost","root",$database_password,"tp_amc_hr");

//If the connection fails, return an error:
if (!$con){
    die('Could not connect: ' . mysqli_connect_errno());
}

//Get employee info of the entered id from the database. If cannot, output an error to user.
//Preparing SQL query to get the employee account information from database:
$get_employee_info = $con->prepare('SELECT user_account_level, password, account_status, password_failed_attempts
 FROM user_accounts WHERE employee_id=?');
$get_employee_info->bind_param('i', $entered_id);
$get_employee_info->execute();

//Get the result of the SQL query, which is the account information of the employeee:
$result = $get_employee_info->get_result();

//If there is no result (rows) returned, that means this employee does not exist in the database:
if ($result->num_rows == 0){
    //Setting session variable msg which stores the error message (that id does not exist in the database)
    //Which would be used in login.php to display the error message:
    $_SESSION['msg'] = encrypt_data("Employee ID not found. Please check again.");
    
    //Form values are converted to query string, then encrypted.
    //Then stored as session variable so that entered id can be displayed in login.php:
    $_SESSION['form_values'] = encrypt_data(http_build_query($_POST));
    header($redirect_location);
    exit();
}

//Initialise variables from the database with variables of the same names:
if (isset($result)) {
    //Get the results in an array with the keys being the database column names:
    $employee_info = $result->fetch_assoc();
    $user_account_level = $employee_info['user_account_level'];
    //Password is encrypted in case database has been accessed by attacker, so can't use retrieved password(s) to login:
    $password = decrypt_data($employee_info['password']);
    $account_status = $employee_info['account_status'];
    $password_failed_attempts = $employee_info['password_failed_attempts'];
}

//Prepare query for log: (to be executed when user account is locked or trying to access locked account)
$post_log = $con->prepare('INSERT INTO activity_log (action, time) VALUES (?, ?)');

//Check if account is locked. If so, output error message to user and log this attempt.
if ($account_status == "locked") {
    //Error message to inform the user that the account they are trying to access is locked:
    $msg = "Account has reached the maximum attempts and is currently locked.
 Please approach HR staff to reset your account.";
    $login_status = false;
    
    //Logging that someone tried to access a locked account.
    $action = "Someone tried to access {$entered_id}'s account when it is locked.";
    $post_log->bind_param('ss', $action, $time);
    $post_log->execute();
    $post_log->close();
}
else {
    //Check if password is correct. If so, reset the failed attempts to 0.
    if ($entered_password == $password){
        $login_status = true;
        $password_failed_attempts = 0;
    } else {
        //Incrementing failed attempts if password entered is not correct:
        $password_failed_attempts += 1;
        $login_status = false;
        
        //If number of failed attempts is now 5, output error message to user and log that this account is locked.
        if ($password_failed_attempts == 5){
            $account_status = 'locked';
            $msg = "Account has reached the maximum attempts and is currently locked.
 Please approach HR staff to reset your account.";
            
            //Log that user account is now locked.
            $action = $entered_id . "'s account is now locked";
            $post_log->bind_param('ss', $action, $time);
            $post_log->execute();
            $post_log->close();
            
        //Else if number of failed attempts is less than 5, error message is that password is incorrect.
        } else {
            $msg = "Password is incorrect.";
        }
    }
}

//Updating the user account table (account status and failed password attempts)
//For example, the user account is now locked, increment failed attempts or resetting failed attempts to 0
$post_user_acct = $con->prepare('UPDATE user_accounts SET account_status=?, password_failed_attempts=?
 WHERE employee_id=?');
$post_user_acct->bind_param('sii', $account_status, $password_failed_attempts, $entered_id);
$post_user_acct->execute();
$post_user_acct->close();

//If password of entered id matches the one in database, login_status will be true and user will be logged in.
if ($login_status){
    
    ini_set("session.gc_maxlifetime", 300);
    
    //Setting session variables user_id, user_level and last activity of user:
    $_SESSION['user_id'] = $entered_id;
    $_SESSION['user_level'] = $user_account_level;
    $_SESSION['last_activity'] = time();
    
    //Unset session variables (msg is the error message, form_values is the id and entered password)
    unset($_SESSION['msg']);
    unset($_SESSION['form_values']);
    
    //Direct user to home page, according to user account level (which have different privileges)
    switch ($user_account_level){
        case "1":
            $con->close();
            header('Location: /swap%20updated%20website/employee_home.php');
            exit();
        case "2":
            $con->close();
            header('Location: /swap%20updated%20website/hr_home.php');
            exit();
        case "3":
            $con->close();
            header('Location: /swap%20updated%20website/boss_home.php');
            exit();
        default:
            $con->close();
            header($redirect_location);
            exit();
    }
} else{
    //Error message and values from the login form are to be encrypted then stored in the session to be called.
    $_SESSION['msg'] = encrypt_data($msg);
    //Form values are converted to query string, then encrypted:
    $_SESSION['form_values'] = encrypt_data(http_build_query($_POST));
    header($redirect_location);
    exit();
}
