Project Title: 
Eevee Specialist Clinic 

Project Description: 
Eevee Specialist Clinic allows specialists and their registrars to perform their daily operations such as booking tests, prescribing and dispensing medicine easily, streamlining their processes

Eevee Specialist Clinic set up: 
The following requirements are needed to set up and use Eevee Specialist Clinic 

Software requirements: 
The following software is required to run Project Eevee Specialist Clinic:
A working version of MAMP / WAMP server 
MySQL version 8.0 and above 
Docker 

The following Programming languages are used for Project Eevee Specialist Clinic:

Backend: 
Python 3.8 onwards 
MySQL 8.0

Frontend:
HTML
PHP
CSS
JavaScript

Frontend Frameworks used:
Bootstrap 
Vue.js
jquery

Dependencies 
If you are running the different microservices on your machine directly without using Docker or any other virtual machine, kindly install the following dependencies 
Python: 
For python, the following are the modules required for this project, including its usage. Inside your terminal, input the following: pip3 install <dependency name> OR python -m pip install <dependency name>

<dependency name>

1) pika - Used for AMQP exchange
2) twilio - Used for sending appointment confirmation to patients
3) socketio - Used for displaying messages from RabbitMQ to UI
4) Flask - Allowing the different microservices to act as an application
5) Flask-SQLAlchemy - Enabling the microservices to access our MySQL Database 
6) MySQL-connector-python - Connecting microservices to our MySQL Database 
7) Flask-Cors - For handling cross-origin resource sharing (CORS) within microservices

import os, sys
import requests

Database setup: 
- With reference to the “sql_files” folder, load the “booking.sql”, "inventory.sql" and "patient.sql" script into your MySQL software, and load 3 databases into your MySQL database.
Running Project Eevee Specialist Clinic 
- All files are configured to run on Windows, e.g. dbURL defined as `dbURL: mysql+mysqlconnector://root@host.docker.internal:3306/bookings` in docker-compose.yml


Ports:
1. booking.py (port 5000)
2. patient.py (port 5051)
3. get_appointments.py (port 5010)
4. notification.py (port 5008)
5. booktest.py (port 5055)
6. prescription_check.py (port 5002)
7. prescribe_medicine.py (port 5101)
8. openfda.py (no port)
9. inventory.py (port 5211)
10. amqp_setup.py (no port)
11. invokes.py (no port)
12. dispense_restock.py (port 5204)
12. RabbitMQ (5672 and 15672)


Using Docker Compose: 
1) Start your MAMP/WAMP Servers 
2) Ensure that any rabbit-m containers are not running as it might conflict with the RabbitMQ container specified in the .yml file. 
3) In a CMD window, change the directory to the highest parent folder which contains the docker-compose.yml file. 
4) In the same CMD window, run the following command: 
5) docker-compose up -d
6) To stop the project from running, run the following command:
7) docker-compose down

==================================================== Eevee Specialist Clinic Step by Step: =================================================================

Pre-setups:
1) Ensure that Eevee Specialist Clinic Setup is completed (above)
2) Ensure that databases is setup with the correct path inside the sql files. 
3) Ensure that <dockerid> inside docker-compose.yml is changed to the user’s dockerid
4) Note that this is a demonstration of our 3 scenarios. New appointments entries have to made after 5th April 2023
in the appointment_history table of the patient_records database, with ApptDateTime having the date you are testing and 
'tbd' as Diagnosis, according to the available patients in the patient table, for the upcoming doctor's appointment to show on the UI

Step by Step Walkthrough:
Scenario 1: Booking a Diagnostic Test:
Pre database setup: Run the stored procedures in the sql database "delete_expired_bookings" and "create_booking_slots" to create the fresh appointment slots for the day.
1) Head to ../Specialist_Page/specialist_page.php (Specialist UI), there will be a table displaying the booked appointment slots for the day
2) For the selected timeslot (row), click on "Book a Test" to book a test
3) Select the test_type for the test and click "Search" button (patient's phone number is retreived).
4) If there are available slots, it will be displayed on the UI page with their timings and bookingID.
5) For the selected timeslot, Click on “Book Test”, now a booking will be made and a message will be sent to the patient's phone.
	(At this point a diagnostic test will be added to diagnostic_history in the patient_records database, and timeslot in the booking database is marked unavailable)

Scenario 2: Prescribing Medicine and Checking for Drug Interactions:
1) Head to ../Specialist_Page/specialist_page.php (Specialist UI), there will be a table displaying the booked appointment slots for the day
2) For the selected timeslot (row), click on "Prescribe Medicine" to prescribe medicine
3) Create prescription by selecting the medicine name, and inputting frequency and dosage amount. Click on "Add medicine" to add more medicine and "Remove" to delete medicine prescription
4) Click on "Prescribe Medicine” and a message will be displayed if there is a problem with the medicine interaction. If not, it will lead the user back to home page. 
(At this point, the "prescription history" will be updated with the patient's prescription information)
5) Click on "Complete Consult" to complete the patient's consult (The appointment slot will be deleted from the appointment history table in patient_records)

Scenario 3: Dispensing Medicine and Restocking Medicine:
1) Head to ../Registrar/Registrar.php  (Registrar UI)
2) Key in a Patient ID (1, 2, or 3 – database is set up for these values)
3) Click the "Get Prescription Details" button. The prescription that needs to be given to the patient today will then appear on the page.
4) If the amount of medicine left in the in-clinic inventory drops below the threshold amount once this patient's prescription is dispensed, an alert will pop up to notify the registrar to put in an order for more medicine.