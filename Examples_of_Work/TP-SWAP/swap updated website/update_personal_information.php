<!DOCTYPE html>
<html lang="en">
<?php
session_start();
include 'check_session.php';
?>
<head>
<meta charset="UTF-8">
<head>
	<title>Update User Information</title>
	<?php include 'shared_css_form.php'; ?>
</head>

<body>
	<?php include "navbar.php";	?>
	
	<form action="update_personal_information_do.php" method="post">
    	<?php
    	
    	include 'shared.php';
    	// Display error message if it exists & gets prev form values
    	if (isset($_SESSION['msg'])) {
    	    $msg = decrypt_data($_SESSION['msg']);
    	    echo "<p style='color: red;'>{$msg}</p>";
    	    $decrypted_query = decrypt_data($_SESSION['form_values']);
    	    //parse query strin into vari and store in array
    	    parse_str($decrypted_query, $data);
    	    unset($_SESSION['msg']);
    	    unset($_SESSION['form_values']);
    	}  else {
    	    //get employee personal info
    	    $user_id=$_SESSION['user_id'];
    	    $con = mysqli_connect("localhost","root",$database_password,"tp_amc_hr"); //connect to database
    	    if (!$con){
    	        die('Could not connect: ' . mysqli_connect_errno()); //return error is connect fail
    	    }
    	    $get_employee_info = $con->query("SELECT contact,email,bank_account FROM
            employee_information WHERE employee_id={$user_id}");
    	    $info = $get_employee_info->fetch_assoc();
    	    $contact = decrypt_data($info['contact']);
    	    $email = decrypt_data($info['email']);
    	    $bank_account = decrypt_data($info['bank_account']);
    	}
    	?>
        <h2>Update User Information</h2>
        <label for="contact">Contact:</label>
        <input type="text" id="contact" name="contact" required
        value="<?php echo isset($contact) ? $contact : $data['contact']; ?>">
    	<br><br>
        <label for="email">Email:</label>
        <input type="text" id="email" name="email" required
        value="<?php echo isset($email) ? $email : $data['email']; ?>">
        <br><br>
        <label for="bank_account">Bank Account:</label>
        <input type="text" id="bank_account" name="bank_account" required
    	value="<?php echo isset($bank_account) ? $bank_account : $data['bank_account']; ?>">
    	<br><br><br>
        <button type="submit" name="submit">Submit</button>
  </form>
</body>
</html>
