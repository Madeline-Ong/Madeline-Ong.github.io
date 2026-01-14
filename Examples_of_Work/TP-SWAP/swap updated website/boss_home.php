<!DOCTYPE html>
<html lang="en">
<?php
session_start();
include 'check_session.php'; 
?>
<head>
    <meta charset="UTF-8">
    <title>Boss Homepage</title>
    <?php include "shared_css_home.php";?>
</head>
<body>
	<?php include "navbar.php"; ?>
  
  <div class="container">
    <a href="list_leave_application.php" class="block" >
      <img src="https://pic.onlinewebfonts.com/thumbnails/icons_129824.svg">
      <h2>Leave Management</h2>
    </a>

    <a href=list_mc_application.php class="block">
      <img src="https://pic.onlinewebfonts.com/thumbnails/icons_563681.svg">
      <h2>MC Management</h2>
    </a>
    
    <a href="personal_information.php" class="block">
      <img src="https://pic.onlinewebfonts.com/thumbnails/icons_559210.svg">
      <h2>Personal Information</h2>
    </a>
    
    <a href="list_employees.php" class="block">
      <img src="https://pic.onlinewebfonts.com/thumbnails/icons_549429.svg">
      <h2>Employee Management</h2>
    </a>
    
    <a href="list_logs.php" class="block">
      <img src="https://pic.onlinewebfonts.com/thumbnails/icons_366472.svg">
      <h2>Logs Management</h2>
    </a>
  </div>

</body>
</html>