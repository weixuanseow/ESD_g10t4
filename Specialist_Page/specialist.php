<?php
session_start(); // start the session
if (!isset($_SESSION['username'])) { 
    header('Location: login.html'); 
    exit;
}
$username = $_SESSION['username']; 
echo "Welcome, $username!";
?>