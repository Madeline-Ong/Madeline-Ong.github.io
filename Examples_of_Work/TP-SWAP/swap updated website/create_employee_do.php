<!-- AUTHOR: JOVAN CHUA RUI CHENG -->
<!-- LAST UPDATED: 18/01/2024 -->
<!-- SUMMARY: THIS FILE TO TAKE VALIDATE AND PARSE IN INPUTS FROM CREATE EMPLOYEE -->

<?php
//Resume the sessions
session_start();

//To include shared.php
include 'shared.php';

//Check if the page was called/redirected from a button from list_employees.php, else redirect to list_employees.php
if (!isset($_POST['submit'])){
    header('Location: /swap updated website/list_employees.php');
    exit();
}

//Get user employee ID from sessions
$user_id = $_SESSION['user_id'];

//Set the varibales from the form
$employee_name = $_POST['employee_name'];
$contact = $_POST['contact'];
$email = $_POST['email'];
$birthday = $_POST['birthday'];
$bank_account = $_POST['bank_account'];
$salary = $_POST['salary'];
$department = strtoupper($_POST['department']);

//Set an array of departments, can further add more if needed
$list_department=array('FINANCE','HR','IT');

//Connect to database and check if the connection fails, return an error
$con = mysqli_connect("localhost","root",$database_password,"tp_amc_hr");
if (!$con){
    die('Could not connect: ' . mysqli_connect_errno());
}

//Search database to see if there is such an employee existing already
$check_employee=$con->prepare('SELECT * FROM employee_information WHERE name = ?');
$check_employee->bind_param('s', $employee_name);
$check_employee->execute();
$employee_result=$check_employee->get_result();
$check_employee->close();

//Set variables to check if employee is older than 18 by using current year and trace back 18 years
$current_year = date('Y');
$above_18 = new DateTime("December 31, $current_year");
$above_18 = $above_18->sub(new DateInterval('P18Y'));
$above_18 = $above_18->format('Y-m-d');


if($employee_result->num_rows != 0){
    //Check if the employee exists in the database
    $msg = "This employee exists in the database. Name should be unique.";
} elseif(!preg_match($check_name, $employee_name)){
    //Validate the name
    $msg = "Employee name should only have letters and space.";
} elseif(!preg_match($check_contact, $contact)){
    //Validate the contact
    $msg = "Contact should only contains 8 numbers and no special characters.";
} elseif(!filter_var($email, FILTER_VALIDATE_EMAIL)){
    //Validate the email
    $msg = "Invalid email format.";
} elseif(!preg_match($check_email,$email)){
    //Validate the email domain
    $msg = "Please only use gmails.";
} elseif($birthday >= $above_18){
    //Validate if employee older than 18
    $msg = "Employee should be older than 18.";
} elseif(!preg_match($check_bank_account,$bank_account)){
    //Validate the bank account
    $msg = "Bank account number should only have numbers and -.";
} elseif(!preg_match($check_salary,$salary)){
    //Validate the salary
    $msg = "Salary should only be whole numbers.";
} elseif(!preg_match($check_department, $department)){
    //Validate the depertment
    $msg = "Department should only contain letters and spaces. Only use existing departments.";
} elseif(!in_array($department,$list_department)){
    //Check if the inputted department exists
    $msg = "Department does not exist.";
} else{
    //If pass checks, encrypt the data and store in database, do not need password as a default password is set
    //in database
    //and employees will be asked to change the default password once the account is created
    $contact = encrypt_data($contact);
    $email = encrypt_data($email);
    $birthday = encrypt_data($birthday);
    $bank_account = encrypt_data($bank_account);
    $salary = encrypt_data($salary);
    
    //Creating new employee in employee_information
    $create=$con->prepare('INSERT INTO employee_information (name, department, contact, email,
    bank_account, birthday, salary) VALUES (?,?,?,?,?,?,?)');
    $create->bind_param('sssssss', $employee_name, $department, $contact, $email, $bank_account, $birthday, $salary);
    
    //If an is employee created in employee_information table, log it and create user acct for new employee
    if ($create->execute()) {
        //Using name to find newly created emloyee ID
        $get_id = $con->prepare('SELECT employee_id FROM employee_information WHERE name = ?');
        $get_id->bind_param('s', $employee_name);
        $get_id->execute();
        $result = $get_id->get_result();
        
        //If employee is created successfully, the query would retrieve the new employee id that was generated in db
        if ($result->num_rows > 0) {
            $row = $result->fetch_assoc();
            $id = $row['employee_id'];
            
            //Log that employee was created successfully
            $post_log = $con->prepare('INSERT INTO activity_log (action, time) VALUES (?, ?)');
            $action = "{$user_id} added a new employee {$id}.";
            $post_log->bind_param('ss', $action, $time);
            $post_log->execute();
            $post_log->close();
            
            //Check for user department, and user employee ID to create a user account fit for their department
            if ($department == "HR") {
                $create_user = $con->prepare('INSERT INTO user_accounts (employee_id, user_account_level) VALUES
                (?, ?)');
                $level = 2;
                $create_user->bind_param('ii', $id, $level);
            } else {
                $create_user = $con->prepare('INSERT INTO user_accounts (employee_id) VALUES (?)');
                $create_user->bind_param('i', $id);
            }
            
            //If user account is created successfully, close the connections and proceed back to list_employees.php
            if ($create_user->execute()) {
                $create_user->close();
                $get_id->close();
                $create->close();
                $con->close();
                header('Location: /swap updated website/list_employees.php');
                exit();
            } else {
                //If user account is not created succesfully
                $msg = "Contact IT. Error inserting into user_accounts.";
            }
        } else {
            //If unable to find the employee we created
            $msg = "Contact IT. No employee found with that name.";
            $get_id->close();
        }
    } else {
        //If unable to create the employee
        $msg = "Contact IT. Error inserting into employee_information.";
    }
    $create->close();
}
//Close database connections and set error message and previous inputted form values to be in sessions, and
//redirect back to create_employee.php
$_SESSION['msg'] = encrypt_data($msg);
$_SESSION['form_values'] = encrypt_data(http_build_query($_POST));

$con->close();
header('Location: /swap updated website/create_employee.php');
exit();
