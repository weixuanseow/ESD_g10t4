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
    <script src="https://unpkg.com/vue@3.2.47/dist/vue.global.js"></script>
    
    <!-- Axios -->
    <script src="https://cdn.jsdelivr.net/npm/axios@1.1.2/dist/axios.min.js"></script>


    <title>Specialist Home Page</title>
    
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
        Appointments
    -->
    <div>
        <h1>Your Appointments</h1>
        <div id="appointment">
            <!--Doctors Appointments-->
            <table id="appointment_table" border="2px">
            <tr>
                <th>
                    <h2>Date&Time</h2>
                </th>

                <th>
                    <h2>Patient</h2>
                </th>

                <th>
                    <h2>Select</h2>
                </th>

            </tr>
            <tr v-for="obj of this.something" id='obj.appt_datetime'>
                <td v-if="obj.appt_datetime.includes(this.datetosearch) && obj.diagnosis == 'tbd' ">{{obj.appt_datetime}}</td>
                <td v-if="obj.appt_datetime.includes(this.datetosearch) && obj.diagnosis == 'tbd' ">{{obj.patient_id}}</td>
                <td v-if="obj.appt_datetime.includes(this.datetosearch) && obj.diagnosis == 'tbd' ">
                    <button class="btn btn-primary m-2" @click="prescribe(obj.appt_datetime, obj.patient_id)">Prescribe Medicine</button>
                    <button class="btn btn-warning m-2"  @click="booking(obj.appt_datetime, obj.patient_id)">Book a Test</button>
                    <button class="btn btn-success m-2"  @click="remove(obj.appt_datetime, obj.patient_id)">Complete Consult</button>
                </td>
            </tr>
        </table>
        </div>
    </div>
    
    <!-- START OF JS IMPORTS (DO NOT ADD ANYTHING BELOW THIS LINE!) ---------------------------------------------------------------------------------------------- -->
        <!-- Font Awesome JS -->
        <script src="https://kit.fontawesome.com/c7ddd7a650.js" crossorigin="anonymous"></script>
        <script src="specialist.js"></script>
        <!-- bootstrap js -->
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/js/bootstrap.min.js" integrity="sha384-IDwe1+LCz02ROU9k972gdyvl+AESN10+x7tBKgc9I5HFtuNz0wWnPclzo6p9vxnk" crossorigin="anonymous"></script>



    </body>
</html>