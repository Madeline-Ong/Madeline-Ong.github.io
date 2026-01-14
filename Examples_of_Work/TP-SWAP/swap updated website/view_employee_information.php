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
	<title>Employee Information</title>
	<?php include 'shared_css.php'; ?>
</head>

<body>
	<?php include "navbar.php"; ?>
	<div class="table_container">
    	<table>
        <?php
        
        $user_id = $_SESSION['user_id'];
        
        //Get the id of the employee the user is trying to view the information of 
        if (isset($_POST['employee_id'])) {
            $employee_id = $_POST['employee_id'];
            $_SESSION['employee_id'] = $employee_id;
        } else {
            $employee_id = $_SESSION['employee_id'];
        }
        
        //To connect to database and if the connection fails, return an error
        $con = mysqli_connect("localhost", "root", $database_password, "tp_amc_hr");
        if (!$con) {
            die('Could not connect: ' . mysqli_connect_errno());
        }
        
        //Displaying employee info as a table
        $get_employee_info = $con->query('SELECT * FROM employee_information WHERE employee_id = ' . $employee_id);
        $get_acct_status = $con->query('SELECT account_status FROM user_accounts WHERE employee_id = ' . $employee_id);
        while (($info = $get_employee_info->fetch_assoc()) && ($stat = $get_acct_status->fetch_assoc())) {
            echo "<tr><td>ID:</td><td>" . $info['employee_id'] . "</td></tr>";
            echo "<tr><td>Name:</td><td>" . $info['name'] . "</td></tr>";
            echo "<tr><td>Department:</td><td>" . $info['department'] . "</td></tr>";
            echo "<tr><td>Birthday:</td><td>" . decrypt_data($info['birthday']) . "</td></tr>";
            echo "<tr><td>Contact:</td><td>" . decrypt_data($info['contact']) . "</td></tr>";
            echo "<tr><td>Email:</td><td>" . decrypt_data($info['email']) . "</td></tr>";
            echo "<tr><td>Bank Account:</td><td>" . decrypt_data($info['bank_account']) . "</td></tr>";
            echo "<tr><td>Salary:</td><td>" . decrypt_data($info['salary']) . "</td></tr>";
            echo "<tr><td>MC days taken:</td><td>" . $info['mc_days_taken'] . "</td></tr>";
            echo "<tr><td>Leave days taken:</td><td>" . $info['leave_days_taken'] . "</td></tr>";
            echo "<tr><td>Status:</td><td>" . $stat['account_status'] . "</td></tr>";
        }
        
        $con->close();
        ?>
    	</table>
	</div>
    <!-- Container for the buttons, to be centered -->
	<div class="button_container">
		<button class="button" id='change_info' onclick="window.location.href='update_employee_information.php'">Change Information</button>
		<button class="button" id="reset" onclick="window.location.href='reset_account_status.php'">Reset Account Status</button>
		<button class="button" id='del'>Delete Employee</button>
	</div>
	<!-- Delete modal with a message for confirmation. User would have to select 'Yes' or 'No' as confirmation. -->
	<div id="delete_modal" class="modal">
		<!-- Modal content -->
		<div class="modal_content">
			<p>Are you sure you want to delete this employee?</p>
			<br>
			<button class="button" onclick="window.location.href='delete_employee.php'">Yes</button>
			<button class="button" id='close'>No</button>
		</div>

	</div>

	<script>
    // boss and current user cannot be deleted
	document.querySelector('#del').style.display = '<?php echo ($employee_id == 1 || $user_id == $employee_id) ? 'none' : 'inline'; ?>';
    
    // boss info cannot be changed, only in personal info
	document.querySelector('#change_info').style.display = '<?php echo $employee_id == 1 ? 'none' : 'inline'; ?>';
	document.querySelector('#reset').style.display = '<?php echo $employee_id == 1 ? 'none' : 'inline'; ?>';
    
    // Get the modal
    var modal = document.getElementById("delete_modal");
    
    // Get the delete button that opens the modal
    var delete_button = document.getElementById("del");
    
    // Get the No button that closes the modal
    var span = document.getElementsByClassName("close")[0];
    
    // When the user clicks the button, open the modal
    delete_button.onclick = function() {
    	modal.style.display = "block";
    }
    
    // When the user clicks on No, close the modal
    close = document.getElementById('close');
    close.onclick = function() {
    	modal.style.display = "none";
    }
    
    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target == modal) {
        	modal.style.display = "none";
        }
    }
    </script>

</body>
</html>