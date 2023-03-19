<?php
session_start(); // start the session
if (!isset($_SESSION['username'])) { 
    header('Location: ../login_page/login.html'); 
    exit;
}

?>