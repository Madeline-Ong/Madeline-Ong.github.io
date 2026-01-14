<?php
$con = mysqli_connect("localhost", "root", $database_password, "tp_amc_hr"); // connect to database
if (!$con) {
    die('Could not connect: ' . mysqli_connect_errno()); // return error is connect fail
}

//Action to be done is depend seraching for what (stored in type)
if (isset($_POST['type'])){
    $where_clause = 'WHERE ';
    // Check if employee_id is set and not empty then add it to where clause
    if (isset($_POST['employee_id']) && !empty($_POST['employee_id'])) {
        $employee_id = $_POST['employee_id'];
        $where_clause .= " employee_id LIKE '%$employee_id%'";
    }
    // Check if status is set then add it to where clause
    if (isset($_POST['status'])) {
        $status = $_POST['status'];
        if ($status != 'all'){
            if (str_contains($where_clause, 'id')){
                $where_clause .= "AND status = '$status'";
            } else{
                $where_clause .= " status = '$status'";
            }
        }
    }
    // Check if department is set then add it to where clause
    if (isset($_POST['department'])) {
        $department = $_POST['department'];
        if ($department != 'all'){
            if (str_contains($where_clause, 'id')){
                $where_clause .= "AND department = '$department'";
            } else{
                $where_clause .= " department = '$department'";
            }
        }
    }
    
    //if none of the above variables are true so no condit, clear the where clause 
    if (!str_contains($where_clause, '_id') && !str_contains($where_clause, 'status')
        && !str_contains($where_clause, 'depart')){
            $where_clause = '';
    }
    
    // search for leave 
    if ($_POST['type'] == 'leave'){
        $get_leave = $con->query('SELECT * FROM leave_application ' . $where_clause);
        $count = 1;
        if ($get_leave->num_rows != 0) {
            while ($row = $get_leave->fetch_assoc()){
                echo '<tr>';
                echo '<td> ' . $count . '</td>';
                echo '<td> ' . $row['employee_id'] . '</td>';
                echo '<td> ' . $row['start_date'] . '</td>';
                echo '<td> ' . $row['end_date'] . '</td>';
                echo '<td> ' . $row['status'] . '</td>';
                echo '<td> <button onclick=more_info(\'' . $row['leave_id'] . '\')>More</button></td>';
                echo '</tr>';
                $count++;
            }
        }
        echo "<script> function more_info(leave_id){
    		// Pass the leave_id to the server using a hidden form input
            var hidden_form = document.createElement('form');
            hidden_form.style.display = 'none';
            hidden_form.method = 'post';
            hidden_form.action = 'view_employee_leave_application.php'; 
        	
        	// Create input and append to form
            var form_input = document.createElement('input');
            form_input.type = 'hidden';
            form_input.name = 'leave_id';
            form_input.value = leave_id;
        	
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
		}</script>";        
    }
    
    // search for mc
    if ($_POST['type'] == 'mc'){
        $get_mc = $con->query('SELECT * FROM mc_application ' . $where_clause);
        $count = 1;
        if ($get_mc->num_rows != 0) {
            while ($row = $get_mc->fetch_assoc()){
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
        echo "<script> function more_info(mc_id){
    		// Pass the leave_id to the server using a hidden form input
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
		}</script>";
    }
    
    // search for employee
    else if ($_POST['type'] == 'employee'){
        $get_employee = $con->query('SELECT * FROM employee_information ' . $where_clause);
        $count = 1;
        if ($get_employee->num_rows != 0) {
            while ($row = $get_employee->fetch_assoc()){
                echo '<tr>';
                echo '<td> ' . $row['employee_id'] . '</td>';
                echo '<td> ' . $row['name'] . '</td>';
                echo '<td> ' . $row['department'] . '</td>';
                echo '<td> ' . decrypt_data($row['email']) . '</td>';
                echo '<td> ' . decrypt_data($row['contact']) . '</td>';
                echo '<td> <button onclick=more_info(\'' . $row['employee_id'] . '\')>More</button></td>';
                echo '</tr>';
                $count++;
            }
        }
        echo "<script> function more_info(employee_id){
    		// Pass the leave_id to the server using a hidden form input
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
		}</script>";
    }
    
    // search for log
    else if($_POST['type'] == 'log'){
        $action = $_POST['action'];
        $get_log = $con->query("SELECT * FROM activity_log WHERE action LIKE '%" . $action . "%'");
        
        $count = 1;
        if ($get_log->num_rows != 0) {
            while ($row = $get_log->fetch_assoc()){
                echo '<tr>';
                echo '<td> ' . $count . '</td>';
                echo '<td> ' . $row['action'] . '</td>';
                echo '<td> ' . $row['time'] . '</td>';
                echo '</tr>';
                $count++;
            }
        }
    }
}

$con->close();