<!-- AUTHOR: JOVAN CHUA RUI CHENG -->
<!-- LAST UPDATED: 18/01/2024 -->
<!-- SUMMARY: THIS FILE TO TAKE IN INPUTS TO CREATE NEW EMPLOYEE -->

<!DOCTYPE html>
<html lang="en">
<?php
//Resume the sessions
session_start();

//To include shared.php and check_session.php
include 'check_session.php';
include 'shared.php';

//Set an array of allowed referers
$allowed_refer=array('list_employees.php','create_employee.php');

//Find out and set what is the refer in the HTTP request
$referring_page=isset($_SERVER['HTTP_REFERER'])? $_SERVER['HTTP_REFERER']:'';

//Check if the referer is from array of allowed referer, else redirect back to list_employees.php
if (!in_array(basename($referring_page), $allowed_refer)){
   header('Location: /swap updated website/list_employees.php');
   exit();
}
?>
<head>
	<meta charset="UTF-8">
	<title>Employee Creation Form</title>
	
	<!-- To use CSS from shared_css_form.php -->
	<?php include 'shared_css_form.php'; ?>
</head>

<body>
    <!-- To use navbar.php -->
	<?php include "navbar.php"; ?>
	
	<!-- Form to take in inputs to create employees -->
	<form action="create_employee_do.php" method="post">
    	<?php
    	//Checks if error message is set in session, and if so display the error message and unset it
        if (isset($_SESSION['msg'])) {
            $msg = decrypt_data($_SESSION['msg']);
        	echo "<p style='color: red;'>{$msg}</p>";
        	    
        	//Set to previous form values and retrieves them
        	$decrypted_query = decrypt_data($_SESSION['form_values']);
        	parse_str($decrypted_query, $data);
        	unset($_SESSION['msg']);
        	unset($_SESSION['form_values']);
        }
        ?>
        	
    		<h2>New Employee</h2>
    		
    		<!-- Input for name -->
    		<label for="employee_name">Name:</label>
    		<input type="text" name="employee_name" id="employee_name" required
    		value="<?php echo isset($data['employee_name']) ? $data['employee_name'] : ''; ?>">
    		<br><br>
    		
    		<!-- Input for contact -->
    		<label for="contact">Contact:</label>
    		<input type="text" name="contact" id="contact" required
    		value="<?php echo isset($data['contact']) ? $data['contact'] : ''; ?>">
    		<br><br>
    		
    		<!-- Input for email -->
    		<label for="email">Email:</label>
    		<input type="text" name="email" id="email" required
    		value="<?php echo isset($data['email']) ? $data['email'] : ''; ?>">
    		<br><br>
    		
    		<!-- Input for birthday -->
    		<label for="birthday">Birthday:</label>
    		<input type="date" name="birthday" id="birthday" required
    		value="<?php echo isset($data['birthday']) ? $data['birthday'] : ''; ?>">
    		<br><br>
    		
    		<!-- Input for bank account -->
    		<label for="bank_account">Bank Account:</label>
    		<input type="text" name="bank_account" id="bank_account" required
    		value="<?php echo isset($data['bank_account']) ? $data['bank_account'] : ''; ?>">
    		<br><br>
    		
    		<!-- Input for salary -->
    		<label for="salary">Salary:</label>
    		<input type="text" name="salary" id="salary" required
    		value="<?php echo isset($data['salary']) ? $data['salary'] : ''; ?>">
    		<br><br>
    		
    		<!-- Input for department -->
    		<label for="department">Department:</label>
    		<input type="text" name="department" id="department" required
    		value="<?php echo isset($data['department']) ? $data['department'] : ''; ?>">
    		
    		<!-- Button to submit -->
    		<button type="submit" name="submit">Submit</button>
		</form>
  	
</body>
</html>
