<!DOCTYPE html>
<html lang="en">
<?php 
session_start();
include 'check_session.php'; 
include 'shared.php';
$user_level = $_SESSION['user_level'];
check_lvl($user_level, 3);
?>
<head>
	<meta charset="UTF-8">
	<title>Logs</title>
	<?php include 'shared_css.php'; ?>
</head>

<body>
	<?php include "navbar.php"; ?>
	<div class="container">
		<h2>List of Logs</h2>
		<div class="action">
			<button class="button" id='del'>Clear logs</button>
		</div>
	</div>
	<div id="confirmation_modal" class="modal">
		<!-- Modal content -->
		<div class="modal_content">
			<p>Are you sure you want to clear the logs from the system?</p>
			<br>
			<button onclick='window.location.href="delete_logs.php"' class="button">Yes</button>
			<button id="close" class="button">No</button>
		</div>
	</div>
	
	<br>
	<div class="table_container">
		<form id='search' method='post'>
    		<input type='hidden' name='type' value='log'>
            <input type='text' placeholder='Search by action' name='action' value='<?php echo isset($_POST['action']) ? htmlspecialchars($_POST['action']) : ''; ?>'>
    		<button type='submit' class='button'>Search</button>
    	</form>
    	<table>
			<tr>
				<th>Log ID</th>
				<th>Action</th>
				<th>Time</th>
			</tr>
			<?php
			if($_SERVER['REQUEST_METHOD'] == 'POST'){
			    include 'search.php';
			} else {
			    $con = mysqli_connect("localhost", "root", $database_password, "tp_amc_hr"); // connect to database
                if (! $con) {
                    die('Could not connect: ' . mysqli_connect_errno()); // return error is connect fail
                }
                
                $get_all_mc = $con->query('SELECT * FROM activity_log');
                
                $count = 1;
                if ($get_all_mc->num_rows != 0) {
                    while ($row = $get_all_mc->fetch_assoc()){
                        echo '<tr>';
                        echo '<td> ' . $count . '</td>';
                        echo '<td> ' . $row['action'] . '</td>';
                        echo '<td> ' . $row['time'] . '</td>'; 
                        echo '</tr>';
                        $count++;
                    }
                }
            }
            ?>
		</table>
	</div>
	<script>
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