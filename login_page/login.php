<?php
session_start(); 
 $_SESSION['username'] = $username; 
 header('Location: ../Specialist_Page/specialist_page.html');
exit;
?>