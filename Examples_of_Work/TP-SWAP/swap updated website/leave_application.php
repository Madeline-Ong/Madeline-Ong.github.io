<!DOCTYPE html>
<html lang="en">
<?php
session_start();
include 'check_session.php';
include 'shared.php';
$user_level = $_SESSION['user_level'];
check_lvl($user_level, 1);
?>
<meta charset="UTF-8">
<head>
    <title>Leave Application Form</title>
    <?php include 'shared_css_form.php'; ?>
</head>
<body>
	<?php include "navbar.php"; ?>
	<form action="create_leave_application.php" method="post">
		<h1>Leave Application</h1>
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
    	}
    	?>
		<label for="start_date">Start Date:</label>
		<input type="date" name="start_date" placeholder="DD-MMM-YYYY" required
		value="<?php echo isset($data['start_date']) ? htmlspecialchars($data['start_date']) : ''; ?>">
		<br><br>
		<label for="end_date">End Date:</label>
		<input type="date" name="end_date" placeholder="DD-MMM-YYYY" required
		value="<?php echo isset($data['end_date']) ? htmlspecialchars($data['end_date']) : ''; ?>">
		<br><br>
		<label for="reason">Reason:</label>
		<textarea name="reason" placeholder="Write your reason for leave here"
		required><?php echo isset($data['reason']) ? htmlspecialchars($data['reason']) : ''; ?></textarea>
		<br><br><br>
		<button type="submit" name="submit">Apply</button>
	</form>
</body>
</html>