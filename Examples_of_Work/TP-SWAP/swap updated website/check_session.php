<!-- AUTHOR: JOVAN CHUA RUI CHENG -->
<!-- LAST UPDATED: 18/01/2024 -->
<!-- SUMMARY: TO CHECK FOR SESSION VALIDITY -->
<?php
//Set time out for 15 minutes
$timeout = 15 * 60; // 15 minutes in seconds

//Set variable for last activity
$lastActivity = isset($_SESSION['last_activity']) ? $_SESSION['last_activity'] : 0;

//If user ID is not set, redirect to login page
if (!isset($_SESSION['user_id'])) {
    echo '<!DOCTYPE html>
<html>
<head>
    <title>Error Message Popup</title>
    <style>
        /* Styling for the pop-up */
        .popup {
            display: none;
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background-color: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 20px;
            border-radius: 5px;
            z-index: 9999;
        }
        
        /* Styling for the close button */
        .close-btn {
            position: absolute;
            top: 5px;
            right: 10px;
            cursor: pointer;
        }
        
        /* Styling for the checkbox - hide it visually */
        .popup-toggle {
            display: none;
        }
        
        /* Styling for displaying pop-up when the checkbox is checked */
        .popup-toggle:checked + .popup {
            display: block;
        }
    </style>
</head>
<body>
        
    <!-- Error message pop-up checkbox -->
    <input type="checkbox" id="errorCheckbox" class="popup-toggle" checked>
        
    <!-- Error message pop-up -->
    <div id="errorPopup" class="popup">
        <span class="close-btn" onclick="document.getElementById("errorCheckbox").checked = false;">&times;</span>
        <p>Invalid session id</p>
    </div>
        
    <!-- Script to redirect back to login.php after a delay (e.g., 3 seconds) -->
    <script>
        setTimeout(function() {
            window.location.href = "login.php";
        }, 3000); // Redirect after 3 seconds (3000 milliseconds)
    </script>
</body>
</html>';
    exit();
}

//Check if session is expired, if expired redirect it back to login page
if (time() - $lastActivity > $timeout) {
    // Session expired, destroy it
    session_unset();
    session_destroy();
    echo '<!DOCTYPE html>
<html>
<head>
    <title>Error Message Popup</title>
    <style>
        /* Styling for the pop-up */
        .popup {
            display: none;
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background-color: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 20px;
            border-radius: 5px;
            z-index: 9999;
        }
        
        /* Styling for the close button */
        .close-btn {
            position: absolute;
            top: 5px;
            right: 10px;
            cursor: pointer;
        }
        
        /* Styling for the checkbox - hide it visually */
        .popup-toggle {
            display: none;
        }
        
        /* Styling for displaying pop-up when the checkbox is checked */
        .popup-toggle:checked + .popup {
            display: block;
        }
    </style>
</head>
<body>
        
    <!-- Error message pop-up checkbox -->
    <input type="checkbox" id="errorCheckbox" class="popup-toggle" checked>
        
    <!-- Error message pop-up -->
    <div id="errorPopup" class="popup">
        <span class="close-btn" onclick="document.getElementById("errorCheckbox").checked = false;">&times;</span>
        <p>Session has expired</p>
    </div>
        
    <!-- Script to redirect back to login.php after a delay (e.g., 3 seconds) -->
    <script>
        setTimeout(function() {
            window.location.href = "login.php";
        }, 3000); // Redirect after 3 seconds (3000 milliseconds)
    </script>
</body>
</html>';
    exit();
}

// Update last activity time
$_SESSION['last_activity'] = time();



?>
