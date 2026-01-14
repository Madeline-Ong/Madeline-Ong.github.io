<!-- AUTHOR: JOVAN CHUA RUI CHENG, MADELINE ONG YING XUAN -->
<!-- LAST UPDATED: 18/01/2024 -->
<!-- SUMMARY: THIS FILE CONTAINS VARIABLES TO BE COMMONLY USED BY DIFFERENT FILES -->

<?php
//Regex used to check for things, it is in the name
//BY: JOVAN
$word_check='/^[a-zA-Z]+(?:\s[a-zA-Z]+)?$/';
$check_id='/^[0-9]+$/';
$check_reason='/^[a-zA-Z0-9]+(?:\s[a-zA-Z0-9]+)?$/';
$check_name=$word_check;
$check_contact='/^[0-9]{8}$/';
$check_email='/^[a-zA-Z0-9._%+-]+@gmail\.com$/';
$check_bank_account='/^[0-9-]+$/';
$check_password = '/^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()_+]).{8,}$/';
$check_salary = '/^[0-9]+$/';
$check_department=$word_check;

//Database password variable
$database_password = "";

//Variable for the time of the system
//BY: MADELINE
$time=date('Y-m-d H:i:s', time());

//Set a error that can redirect user back to login page
//BY: JOVAN
$redirect_error='<!DOCTYPE html>
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
        <p>Unauthorized access.</p>
    </div>
    
    <!-- Script to redirect back to login.php after a delay (e.g., 3 seconds) -->
    <script>
        setTimeout(function() {
            window.location.href = "login.php";
        }, 3000); // Redirect after 3 seconds (3000 milliseconds)
    </script>
</body>
</html>';

//Function to check user account level before they can access things
//BY: JOVAN
function check_lvl($user_level, $option){
   global $redirect_error;
    //option 1 is checking for boss
    if ($option == 1){
        if ($user_level == 3){
        // unset cause variable not auto unset when session destroyed
        session_unset();
        // Destroy the session
        session_destroy();
        echo $redirect_error;
        exit();
        }
    } elseif ($option == 2) {
        if ($user_level == 1){
            // unset cause variable not auto unset when session destroyed
            session_unset();
            // Destroy the session
            session_destroy();
            echo $redirect_error;
            exit();
        }
    } elseif($option == 3){
        if($user_level != 3){
            // unset cause variable not auto unset when session destroyed
            session_unset();
            // Destroy the session
            session_destroy();
            echo $redirect_error;
            exit();
        }
    }
    
}

// By: MADELINE
function error_display(){
    $msg = decrypt_data($_SESSION['msg']);
    echo "<p style='color: red;'>{$msg}</p>";
    $decrypted_query = decrypt_data($_SESSION['form_values']);
    //parse query strin into vari and store in array
    parse_str($decrypted_query, $data);
    unset($_SESSION['msg']);
    unset($_SESSION['form_values']);
    return $data;
}

// Encrypt data using AES-256-CBC
//By: MADELINE
function encrypt_data($data){
    $key = hex2bin("2ccb83a1c10a244b9bdfbf529f75b55077146108061291f8ad4e48abd1ce9533");
    $iv = random_bytes(16);
    $cipher = "AES-256-CBC";
    $encrypted_data = openssl_encrypt($data, $cipher, $key, 0, $iv);
    
    // Concatenate encrypted data and Initialization Vector (IV), and then base64 encode
    return base64_encode($iv . $encrypted_data);
}

// Decrypt data using AES-256-CBC
// By: MADELINE
function decrypt_data($encrypted_data) {
    $cipher = "AES-256-CBC";
    $key = hex2bin("2ccb83a1c10a244b9bdfbf529f75b55077146108061291f8ad4e48abd1ce9533");
    
    // Extract IV from the first 16 bytes of the encoded ciphertext
    $iv = substr(base64_decode($encrypted_data), 0, 16);
    
    // Extract ciphertext (excluding IV) and decrypt
    $ciphertext = substr(base64_decode($encrypted_data), 16);
    
    return openssl_decrypt($ciphertext, $cipher, $key, 0, $iv);
}


// Check if date is valid
// By: MADELINE
function date_check($date){
    list($year, $month, $day) = explode('-', $date);
    
    //check if year is this year or next:
    if ($year != date('Y') && $year != (date('Y') + 1)){
        return false;
    }
    
    $date = new DateTime($date);
    $today = new DateTime();
    
    //checks if date is later on or today:
    if ($date->format('Y-m-d') >= $today->format('Y-m-d')){
        return $date;
    } else {
        return false;
    }
    
}
?>
