<?php
session_start(); 
$_SESSION['username'] = $_GET['username']; 
header('Location: ../Specialist_Page/specialist_page.php');
#echo $_SESSION['username'];
exit;
?>

