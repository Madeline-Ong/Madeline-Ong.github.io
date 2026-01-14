<!DOCTYPE html>
<html lang="en">
<?php 
session_start();
include 'check_session.php'; 
include 'shared.php';
$user_level = $_SESSION['user_level'];
check_lvl($user_level, 2);

?>
<head>
<meta charset="UTF-8">
<head>
	<title>Update User Information</title>
	<?php include 'shared_css_form.php'; ?>
</head>

<body>
	<?php 
	include "navbar.php"; 
	?>
	<form action="update_employee_information_do.php" method="post">
		<?php 

		// Display error message if it exists & gets prev form values
		if (isset($_SESSION['msg'])) {
		    $msg = decrypt_data($_SESSION['msg']);
		    echo "<p style='color: red;'>{$msg}</p>";
		    $decrypted_query = decrypt_data($_SESSION['form_values']);
		    //parse query strin into vari and store in array
		    parse_str($decrypted_query, $data);
		    unset($_SESSION['msg']);
		    unset($_SESSION['form_values']);
		} else {
		    //get employee current info
		    $employee_id=$_SESSION['employee_id'];
		    
		    $con = mysqli_connect("localhost","root",$database_password,"tp_amc_hr"); //connect to database
		    if (!$con){
		        die('Could not connect: ' . mysqli_connect_errno()); //return error is connect fail
		    }
		    $get_employee_info = $con->query("SELECT salary,department FROM employee_information WHERE employee_id={$employee_id}");
		    $info = $get_employee_info->fetch_assoc();
		    $salary = decrypt_data($info['salary']);
		    $department = $info['department'];
		}
		?>
		<h2>Update Employee Information</h2>
		<label for="salary">Salary:</label> 
		<input type="text" name="salary" id="salary" required
		value="<?php echo isset($salary) ? $salary : ''; ?>"> 
		<br><br> 
		<label for="department">Department:</label> 
		<input type="text" name="department" id="department" required
		value="<?php echo isset($department) ? $department : ''; ?>">
		<br><br><br>
		<button type="submit">Submit</button>
	</form>
</body>
</html>