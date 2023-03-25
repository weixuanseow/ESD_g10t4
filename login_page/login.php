<?php
session_start(); 
$_SESSION['username'] = $_GET['username']; 
header('Location: ../Specialist_Page/specialist_page.vue');
#echo $_SESSION['username'];
exit;
?>

