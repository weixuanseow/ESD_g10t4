<?php
    session_start();
    $username = $_SESSION["username"]
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">

    <!-- local css -->
    <link rel="stylesheet" href="../css/specialistpage.css">
    <link rel="stylesheet" href="../css/general.css">

    <!-- bootstrap css -->
    <link href="/css/main.min.css" rel="stylesheet">

    <!-- external js file
    <script type="module" src="#"></script> -->

    <!-- vue script -->
    <script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
    
    <!-- Axios -->
    <script src='https://unpkg.com/axios/dist/axios.js'></script>


    <title>Registrar Page</title>
    
</head>

<body id="specialistlogin">
    <nav id="navbarspecialist" class="navbar sticky-top navbar-light">

        <!-- Website Name -->
        <a class="navbar-brand ">
            <div class="row" style="margin:0;">
                <div class="col">
                    <iframe src="https://embed.lottiefiles.com/animation/107925"></iframe>
                </div>
                <div class="col my-auto">
                    <form method="GET" >
                        <h4>
                            WELCOME, <?php echo $username; ?>
                        </h4>
                    </form>
                </div>

            </div>
        </a>

        <!-- Menu Icon -->
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        
        <!-- NavBar Items -->
        <div class="collapse navbar-collapse" id="navbarNavDropdown">
            <ul class="navbar-nav" id="navbar">
                <li class="nav-item">
                    <a class="nav-link" aria-current="page" href="#">Home</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="../booking/booking.html">Book a Test</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#">Prescribe Medicine</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#">Dispense and Restock</a>
                </li>
            </ul>
        </div>
    </nav>

    <!--
        To Dispense
    -->
    <h1 style="margin: 20px">To be Dispensed</h1>
    <div id="dispense" style="padding:0px 20px">
        <!-- <form method="GET" action="/get_medicines/"> -->
        Please enter incoming patient ID: <input type="text" id="patient_id"><br>
        <button class="btn btn-primary" id="prescription" @click="get_medicines(this.patient_id)" type="submit">Get Prescription Details</button>
        <!-- </form> -->
    </div>
    <div id="medicines">
        
    </div>
    
    <!-- START OF JS IMPORTS (DO NOT ADD ANYTHING BELOW THIS LINE!) ---------------------------------------------------------------------------------------------- -->
        <!-- Font Awesome JS -->
        <script src="https://kit.fontawesome.com/c7ddd7a650.js" crossorigin="anonymous"></script>
        <script src="registrar.js"></script>
        <!-- bootstrap js -->
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/js/bootstrap.min.js" integrity="sha384-IDwe1+LCz02ROU9k972gdyvl+AESN10+x7tBKgc9I5HFtuNz0wWnPclzo6p9vxnk" crossorigin="anonymous"></script>


    </body>
</html>