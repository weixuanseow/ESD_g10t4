<?php
session_start(); 
$_SESSION['username'] = $_GET['username']; 
if($_SESSION['username'] == 'DOCTOR LEK') {
    header('Location: ../Specialist_Page/specialist_page.php');
}
else {
    header('Location: ../Registrar_page/Registrar.php');
}
#echo $_SESSION['username'];
exit;
?>

