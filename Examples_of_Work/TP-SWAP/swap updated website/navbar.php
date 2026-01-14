<!-- AUTHOR: JOVAN CHUA RUI CHENG -->
<!-- LAST UPDATED: 18/01/2024 -->
<!-- SUMMARY: NAVIGATION BAR FOR THE HR WEBSITE -->

<!DOCTYPE html>
<html>
<head>
<!--  Styling for the navbar -->
    <style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
        }
        header {
            background-color: #333;
            color: white;
            text-align: center;
            padding: 10px 0;
        }
        nav {
            background-color: #333;
            padding: 10px 0;
            height: 60px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        nav .title {
            font-size: 24px;
            font-weight: bold;
            color: white;
            margin-left: 40px;
        }
        nav ul {
            list-style-type: none;
            margin: 0;
            padding: 0;
            display: flex;
        }
        nav ul li {
            margin: 0 10px;
        }
        nav ul li:last-child {
            margin-right: 40px;
        }
        nav ul li a {
            text-decoration: none;
            color: white;
            padding: 8px 16px;
        }
        nav ul li a:hover {
            background-color: #555;
        }
    </style>
</head>
<body>
    <nav>
        <div class="title">
            TPAMC HR PORTAL
        </div>
        <ul>
            <?php
                // Check if the user is logged in and their role/permission,
                //and based on user level show the necessary items
                if ($_SESSION['user_level'] === 1) {
                    echo '<li><a href="employee_home.php">Home</a></li>';
                    echo '<li><a href="leave_view.php">Leave Application</a></li>';
                    echo '<li><a href="mc_view.php">MC Application</a></li>';
                    echo '<li><a href="personal_information.php">
                    Personal Information</a></li>';
                } elseif ($_SESSION['user_level'] === 2) {
                    echo '<li><a href="hr_home.php">Home</a></li>';
                    echo '<li><a href="leave_view.php">Leave Application</a></li>';
                    echo '<li><a href="mc_view.php">MC Application</a></li>';
                    echo '<li><a href="personal_information.php">Personal Information</a></li>';
                    echo '<li><a href="list_employees.php">Employee Management</a></li>';
                } elseif ($_SESSION['user_level'] === 3) {
                    echo '<li><a href="boss_home.php">Home</a></li>';
                    echo '<li><a href="list_leave_application.php">Leave Management</a></li>';
                    echo '<li><a href="list_mc_application.php">MC Management</a></li>';
                    echo '<li><a href="personal_information.php">Personal Information</a></li>';
                    echo '<li><a href="list_employees.php">Employee Management</a></li>';
                    echo '<li><a href="list_logs.php">Logs Management</a></li>';
                } else {
                    echo "error";
                }
            ?>
            <li><a href="logout.php">Logout</a></li>
        </ul>
    </nav>
</body>
</html>
