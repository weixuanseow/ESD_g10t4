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
With reference to the “database” folder, load the “ESD_T1.sql” script into your MySQL software, ensuring that the path stated inside the “load data in file” statements of “ESD_T1.sql” is changed.
The file path should be pointing towards the respective .txt files inside of the “data” folder located inside the “database” folder. 
Once changed, run the script to load “ESD_T1” into your MySQL database.
Running Project HawkerMeetsYou

Ports:
1. order.py (port 5000)
2. customer.py (port 5900)
3. hawker (GoLang) (port 5902)
4. driver.py (port 5901)
5. find_driver.py (port 5101)
6. place_order.py (port 5100)
7. prepare_order.py (port 5102)
8. payment.py (port 5001)
9. SendEmail.py (no port)
10. AMQP_setup.py (no port)
11. invokes.py (no port)
12. RabbitMQ (5672 and 15672)

Using Docker Compose: 
1) Start your MAMP/WAMP Servers 
2) Ensure that any rabbit-m containers are not running as it might conflict with the RabbitMQ container specified in the .yml file. 
3) In a CMD window, change the directory to the “Microservices” folder which will contain the docker-compose.yml file. 
4) Change all of the <dockerid> inside the docker-compose.yml file to your own Docker ID 
5) In the same CMD window, run the following command: 
6) docker-compose up -d
7) To stop the project from running, run the following command:
8) docker-compose down

Eevee Specialist Clinic Step by Step:

Pre-setups:
1) Ensure that Eevee Specialist Clinic Setup is completed (above)
2) Ensure that database is setup with the correct path inside ESD_T1.sql
3) Ensure that <dockerid> inside docker-compose.yml is changed to the user’s dockerid

Step by Step Walkthrough:
Booking a Diagnostic Test:
1) Head to /templates/index.html (Specialist UI)
2) Choose a hawker to purchase from by clicking on one of the images
3) Select hawker food to purchase by clicking on “add to cart”
4) Once satisfied with the items, click on “Cart” on the top right corner
5) Click on “Go to checkout”, now a delivery order will be sent to the Driver UI for Drivers to Accept
	(At this point a new order will be added to customer_order in the database)

Prescribing Medicine and Checking for Drug Interactions:
1) Head to /templates/driverUI.html (Specialist UI)
2) Click on “Accept Delivery” and “ok”. (Please wait for at least 3 seconds before clicking the next button)
	(At this point the order_status for customer_order in database should be changed to “DELIVERING” and driver_id should be updated from NULL)
3) Click on “Order Delivered” and “ok”. Once an order is delivered, the payment link will be sent to the customer’s email address.
	(At this point the order_status for customer_order in database should be changed to “DELIVERED”)

Dispensing Medicine and Restocking Medicine:
1) Head to /templates/driverUI.html (Registrar UI)
2) Look for the latest email sent by “hawkermeetsyou@gmail.com”, copy and paste the stripe payment link on a new google chrome tab, 
	i.e. https://buy.stripe.com/test_eVa7uGcjX8rmeOI2cG
3) For payment failure, use any email, 4000 0000 0000 0002, any future date, CVC and name and click “Pay”
4) For payment success, use any email, 4242 4242 4242 4242, any future date, CVC and name and click “Pay”
5) A successful payment will redirect you to the microservices/payment/success.html page.
	(At this point the payment_status for customer_order in database should be changed to “PAID”)
