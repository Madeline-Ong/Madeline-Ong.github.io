<?php
//AUTHOR: MADELINE ONG YING XUAN
//LAST UPDATED: 19/01/2024
//SUMMARY: THIS FILE LOGS THE USER OUT OF THEIR ACCOUNT WHEN THEY ARE LOGGED IN CURRENTLY ON THE HR WEBSITE

//Session is resumed so can retrieve the session variables to be used:
session_start();

//Include code from shared.php:
include 'shared.php';

//Retrieving user_id of the account logged in from session variable:
$user_id = $_SESSION['user_id'];

//Session variables are unset as sometimes variables stored do not unset when the session is destroyed:
session_unset();

// Destroy the session
session_destroy();

//Redirect to the login php
header('Location: /swap%20updated%20website/login.php');
exit();