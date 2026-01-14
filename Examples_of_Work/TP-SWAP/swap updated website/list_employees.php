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
	<title>List of Employees</title>
	<?php include 'shared_css.php'; ?>
</head>

<body>
	<?php include "navbar.php"; ?>
	<div class="container">
		<h2>List of Employees</h2>
		<form action="create_employee.php" method="post">
			<button class="button" type="submit" name="submit">Create Employee</button>
		</form>		
	</div>
	<div class="table_container">
		<!-- seraching for employee -->
    	<form id='search' method='post'>
    		<input type='hidden' name='type' value='employee'>
            <input type='number' placeholder='Search by ID' name='employee_id' value='<?php echo isset($_POST['employee_id']) ? htmlspecialchars($_POST['employee_id']) : ''; ?>'>
            <select name='department'>
                <option value='all' <?php echo (isset($_POST['department']) && $_POST['department'] == 'all') ? 'selected' : ''; ?>>All</option>
                <option value='HR' <?php echo (isset($_POST['department']) && $_POST['department'] == 'HR') ? 'selected' : ''; ?>>HR</option>
                <option value='IT' <?php echo (isset($_POST['department']) && $_POST['department'] == 'IT') ? 'selected' : ''; ?>>IT</option>
                <option value='Finance' <?php echo (isset($_POST['department']) && $_POST['department'] == 'Finance') ? 'selected' : ''; ?>>Finance</option>
            </select>
            <button type='submit' class="button">Submit</button>
    	</form>
    	
		<!-- table of employee listed -->
		<table>
			<tr>
				<th>Employee ID</th>
				<th>Name</th>
				<th>Department</th>
				<th>Email</th>
				<th colspan="2">Contact</th>
			</tr>
			<?php
			//if serach bar above is used (post), then use search.php to display result
			//else display all employees
			if($_SERVER['REQUEST_METHOD'] == 'POST'){
			    include 'search.php';
			} else {
			    $con = mysqli_connect("localhost", "root", $database_password, "tp_amc_hr"); // connect to database
                if (! $con) {
                    die('Could not connect: ' . mysqli_connect_errno()); // return error is connect fail
                }
                
                $get_all_employees = $con->query('SELECT * FROM employee_information');
                if ($get_all_employees->num_rows != 0) {
                    while ($row = $get_all_employees->fetch_assoc()){
                        echo '<tr>';
                        echo '<td> ' . $row['employee_id'] . '</td>';
                        echo '<td> ' . $row['name'] . '</td>'; 
                        echo '<td> ' . $row['department'] . '</td>';
                        echo '<td> ' . decrypt_data($row['email']) . '</td>';
                        echo '<td> ' . decrypt_data($row['contact']) . '</td>';
                        echo '<td> <button onclick=more_info(\'' . $row['employee_id'] . '\')>More</button></td>';
                        echo '</tr>';
                    }
                }
			}
            ?>
            
		</table>
	</div>
	<script>
    	function more_info(employee_id){
    		// Pass the employee_id to the server using a hidden form input
            var hidden_form = document.createElement('form');
            hidden_form.style.display = 'none';
            hidden_form.method = 'post';
            hidden_form.action = 'view_employee_information.php'; 
        	
        	// Create input and append to form
            var form_input = document.createElement('input');
            form_input.type = 'hidden';
            form_input.name = 'employee_id';
            form_input.value = employee_id;
        	
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
	</script>
	
</body>
</html>