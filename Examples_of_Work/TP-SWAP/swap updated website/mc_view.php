<!DOCTYPE html>
<html lang="en">
<?php 
session_start();
include 'check_session.php'; 
include 'shared.php';
$user_level = $_SESSION['user_level'];
check_lvl($user_level, 1);
?>
<head>
    <title>MC Applications</title>
    <?php include 'shared_css.php'; ?>
</head>
<body>
	<?php include "navbar.php"; ?>
	<div class="container">
		<h2>List of MC Applications</h2>
		<div class="action">
			<a class="button" href="mc_application.php">Apply for MC</a>
		</div>
	</div>
	<div class="table_container">
		<table>
			<tr>
				<th>MC ID</th>
				<th>Start Date</th>
				<th>End Date</th>
				<th>Status</th>
			</tr>
			<?php
            $user_id = $_SESSION['user_id'];
            
            $con = mysqli_connect("localhost", "root", $database_password, "tp_amc_hr"); // connect to database
            if (! $con) {
                die('Could not connect: ' . mysqli_connect_errno()); // return error is connect fail
            }
            
            $get_employee_mc = $con->query('SELECT * FROM mc_application WHERE employee_id = ' . $user_id);
            $con->close();
            
            //Display mc application in table
            if ($get_employee_mc->num_rows != 0) {
                $rows = $get_employee_mc->fetch_all(MYSQLI_ASSOC);
                $rows = array_reverse($rows);
                $count = 1;
                foreach ($rows as $row) {
                    echo '<tr>';
                    echo '<td> ' . $count . '</td>';
                    echo '<td> ' . $row['start_date'] . '</td>'; 
                    echo '<td> ' . $row['end_date'] . '</td>'; 
                    echo '<td> ' . $row['status'] . '</td>'; 
                    echo '</tr>';
                    $count++;
                }
            }            
            ?>
		</table>
	</div>
</body>
</html>