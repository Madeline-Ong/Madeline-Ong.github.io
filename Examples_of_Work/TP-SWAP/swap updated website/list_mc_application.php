<!DOCTYPE html>
<html lang="en">
<?php 
session_start();
include 'check_session.php'; 
?>
<head>
	<meta charset="UTF-8">
	<title>MC Applications</title>
	<?php include 'shared_css.php'; ?>
</head>

<body>
	<?php include "navbar.php"; ?>
	<div class="container">
		<h2>List of MC Applications</h2>
		<div class="action">
			<button id='del' class="button">Delete approved/rejected MCs</button>
		</div>
	</div>
	<div id="confirmation_modal" class="modal">
		<!-- Modal content -->
		<div class="modal_content">
			<p>Are you sure you want to delete all approved and rejected leave from the system?</p>
			<br>
			<button onclick='window.location.href="delete_approved_rejected_mc.php"' class="button">Yes</button>
			<button id="close" class="button">No</button>
		</div>
	</div>
	<br>
	<div class='table_container'>
    	<form id='search' method='post'>
    		<input type='hidden' name='type' value='mc'>
            <input type='number' placeholder='Search by Employee ID' name='employee_id' value='<?php echo isset($_POST['employee_id']) ? htmlspecialchars($_POST['employee_id']) : ''; ?>'>
            <select name='status'>
                <option value='all' <?php echo (isset($_POST['status']) && $_POST['status'] == 'all') ? 'selected' : ''; ?>>All</option>
                <option value='pending' <?php echo (isset($_POST['status']) && $_POST['status'] == 'pending') ? 'selected' : ''; ?>>Pending</option>
                <option value='approved' <?php echo (isset($_POST['status']) && $_POST['status'] == 'approved') ? 'selected' : ''; ?>>Approved</option>
                <option value='rejected' <?php echo (isset($_POST['status']) && $_POST['status'] == 'rejected') ? 'selected' : ''; ?>>Rejected</option>
            </select>
            <button type='submit' class='button'>Search</button>
    	</form>
    	<?php
    	include 'shared.php';
    	// Display error message if it exists & gets prev form values
    	if (isset($_SESSION['msg'])) {
    	    $msg = decrypt_data($_SESSION['msg']);
    	    echo "<p style='color: red;'>{$msg}</p>";
    	    unset($_SESSION['msg']);
    	}  
    	?>
    	<table>
			<tr>
				<th>MC ID</th>
				<th>Employee ID</th>
				<th>Start Date</th>
				<th>End Date</th>
				<th colspan="2">Status</th>
			</tr>
			<?php
			if($_SERVER['REQUEST_METHOD'] == 'POST'){
			    include 'search.php';
			} else {
			    $con = mysqli_connect("localhost", "root", $database_password, "tp_amc_hr"); // connect to database
                if (! $con) {
                    die('Could not connect: ' . mysqli_connect_errno()); // return error is connect fail
                }
                
                $get_all_mc = $con->query('SELECT * FROM mc_application');
                
                $count = 1;
                if ($get_all_mc->num_rows != 0) {
                    while ($row = $get_all_mc->fetch_assoc()){
                        echo '<tr>';
                        echo '<td> ' . $count . '</td>';
                        echo '<td> ' . $row['employee_id'] . '</td>';
                        echo '<td> ' . $row['start_date'] . '</td>'; 
                        echo '<td> ' . $row['end_date'] . '</td>';
                        echo '<td> ' . $row['status'] . '</td>';
                        echo '<td> <button onclick=more_info(\'' . $row['mc_id'] . '\')>More</button></td>';
                        echo '</tr>';
                        $count++;
                    }
                }
            }
            ?>
        </table>
	</div>
	<script>
    	function more_info(mc_id){
    		// Pass the mc_id to the server using a hidden form input
            var hidden_form = document.createElement('form');
            hidden_form.style.display = 'none';
            hidden_form.method = 'post';
            hidden_form.action = 'view_employee_mc_application.php'; 
        	
        	// Create input and append to form
            var form_input = document.createElement('input');
            form_input.type = 'hidden';
            form_input.name = 'mc_id';
            form_input.value = mc_id;
        	
            hidden_form.appendChild(form_input);
        	
            // Create submit button and append to form
            var submit_button = document.createElement('button');
            submit_button.type = 'submit';
            submit_button.name = 'submit'; 
        	
            hidden_form.appendChild(submit_button);
        	
            // Append form to body
            document.body.appendChild(hidden_form);
        	
            // Submit form using submit button
            submit_button.click();
		}
		
		// Get the modal
		var modal = document.getElementById("confirmation_modal");
	
		// Get the delete button that opens the modal
		var delete_button = document.getElementById("del");
	
		
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