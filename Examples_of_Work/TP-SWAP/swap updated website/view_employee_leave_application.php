<!DOCTYPE html>
<html lang="en">
<?php 
session_start();
include 'check_session.php'; 
?>
<head>
	<meta charset="UTF-8">
	<title>View Employee Leave</title>
	<?php include 'shared_css.php'; ?>
</head>

<body>
	<?php include "navbar.php"; ?>
	<div class="container">
		<h2>Employee Leave</h2>
	</div>
	
	<div class="table_container">
		<table>
        <?php
            include 'shared.php';
            
            if (isset($_POST['submit'])) {
                $leave_id = $_POST['leave_id'];
                $_SESSION['leave_id'] = $leave_id;
            }
            else {
                exit();
            }
            
            $con = mysqli_connect("localhost", "root", $database_password, "tp_amc_hr"); // connect to database
            if (! $con) {
                die('Could not connect: ' . mysqli_connect_errno()); // return error is connect fail
            }
            $get_leave_info = $con->query('SELECT * FROM leave_application
WHERE leave_id=' . $leave_id);
            
            //displaying leave details
            $leave = $get_leave_info->fetch_assoc();
            $get_leave_info->close();
            $get_employee_name = $con->query('SELECT name FROM employee_information
WHERE employee_id=' . $leave['employee_id']);
            $name = $get_employee_name->fetch_row()[0];
            $get_employee_name->close();
            
            echo "<tr><td>Employee ID:</td><td>" . $leave['employee_id'] . "</td></tr>";
            echo "<tr><td>Name:</td><td>" . $name . "</td></tr>";
            echo "<tr><td>Start Date:</td><td>" . $leave['start_date'] . "</td></tr>";
            echo "<tr><td>End Date:</td><td>" . $leave['end_date'] . "</td></tr>";
            echo "<tr><td>Reason:</td><td>" . $leave['reason'] . "</td></tr>";
            echo "<tr><td>Status:</td><td>" . $leave['status'] . "</td></tr>";
            
            $con->close();
            ?>
    	</table>
    	
    	<div class="button_container">
            <button onclick="open_modal('approve')" class="button">Approve</button> 
            <button onclick="open_modal('reject')" class="button">Reject</button>
        </div>
    	
    	<div id="confirmation_modal" class="modal">
    		<div class="modal_content">
    			<p id="modal_message"></p>
    			<div class="button_container">
        			<button id="confirm_button" class="button">Confirm</button>
        			<button id="cancel_button" onclick="close_modal()" class="button">Cancel</button>
        		</div>
    		</div>
    	</div>
    	
    	<script>
    	// if status of leave is approved or rejected, the buttons not visible
        document.querySelector('.button_container').style.display = '<?php echo ($leave['status'] == 'approved' || $leave['status'] == 'rejected') ? 'none' : 'block'; ?>';
    	
    	var current_action; //to store action
    	var modal = document.getElementById('confirmation_modal');
    	
    	function open_modal(action) {
    		current_action = action;
    		
    		// set modal msg based on action
    		var modal_message = action === 'approve' 
    		? 'Are you sure you want to approve this leave?' 
    		: 'Are you sure you want to reject this leave?';
    		
    		document.getElementById('modal_message').innerText = modal_message;
    		
    		// show modal
    		modal.style.display = "block";
    	}
    	
    	function close_modal() {
    		modal.style.display = 'none';
    	}
    
    	// Add event listener to Confirm button
    	document.getElementById('confirm_button').addEventListener('click', function() {
    		// Handle based on whats current_action
    		if (current_action === 'approve') {
    			window.location.href = 'approve_leave.php';
    		} else if (current_action === 'reject') {
    			window.location.href = 'reject_leave.php';
    		}
    		
    		// Close modal after action
    		close_modal();
    	});
    	
    	// If user clicks anywhere outside of modal, close it
    	window.onclick = function(event) {
    		if (event.target == modal) {
    			modal.style.display = "none";
    		}
    	}
    	
    	window.addEventListener('beforeunload', function() {
    		// Perform an action before the user leaves the page
    		window.location.href = 'unset_session_var.php?var=' + encodeURIComponent('leave_id');
    	});
    	
    </script>
	</div>
</body>
</html>