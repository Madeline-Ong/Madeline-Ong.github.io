<!DOCTYPE html>
<html lang="en">
<?php 
session_start();
include 'check_session.php'; 
?>
<head>
<meta charset="UTF-8">
<title>Personal Information</title>
<?php include 'shared_css.php'; ?>
</head>
<body>
	<?php
	include "navbar.php";
	?>
	<div class="container">
		<h2>Personal Information</h2>
	</div>
	
	<div class="table_container">
		<table>
          <?php
        include 'shared.php';
        $user_id = $_SESSION['user_id'];

        $con = mysqli_connect("localhost", "root", $database_password, "tp_amc_hr"); // connect to database
        if (! $con) {
            die('Could not connect: ' . mysqli_connect_errno()); // return error is connect fail
        }

        // Get employee information
        $get_employee_information = $con->query('SELECT * FROM employee_information WHERE employee_id = ' . $user_id);

        if ($get_employee_information->num_rows == 0) {
            echo "<tr><td colspan='2'>No data found</td></tr>";
            echo $user_id;
        } else {
            $employee_information = $get_employee_information->fetch_assoc();
            $name = $employee_information['name'];
            $department = $employee_information['department'];
            $birthday = decrypt_data($employee_information['birthday']);
            $contact = decrypt_data($employee_information['contact']);
            $email = decrypt_data($employee_information['email']);
            $bank_account = decrypt_data($employee_information['bank_account']);
            $salary = decrypt_data($employee_information['salary']);

            echo "<tr><td>ID:</td><td>" . $user_id . "</td></tr>";
            echo "<tr><td>Name:</td><td>" . $name . "</td></tr>";
            echo "<tr><td>Department:</td><td>" . $department . "</td></tr>";
            echo "<tr><td>Birthday:</td><td>" . $birthday . "</td></tr>";
            echo "<tr><td>Contact:</td><td>" . $contact . "</td></tr>";
            echo "<tr><td>Email:</td><td>" . $email . "</td></tr>";
            echo "<tr><td>Bank Account:</td><td>" . $bank_account . "</td></tr>";
            echo "<tr><td>Salary:</td><td>" . $salary . "</td></tr>";
        }

        $con->close();
        ?>
        
  	</table>
	</div>
	<div class="button_container">
        <form action="update_personal_information.php" method="post">
            <button class="button" name="submit" type="submit">Change Information</button>
        </form>
        <form action="otp_generate.php" method="post">
            <button class="button" name="submit_button" type="submit">Change Password</button>
        </form>
    </div>
</body>
</html>