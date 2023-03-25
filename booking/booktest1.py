from flask import Flask, request, jsonify
from flask_cors import CORS
from invokes import invoke_http
from twilio.rest import Client

import os, sys
# import amqp_setup
# import pika
import json
import requests

app = Flask(__name__)
CORS(app)


@app.route("/book_test1", methods=['POST'])
def book_test():
    # Simple check of input format and data of the request are JSON
    print("======================================book_test.pyr.py - book_test function================================")
    if request.is_json:
        try:
            booking = request.get_json()
            # pid = booking['pid']
            # phone = booking['phone']
            # visit_type = booking['visit_type']
            print("\nReceived a booking in JSON:", )

            # do the actual work
            # 1. Send order info {cart items}
            result = processBooking(booking)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "booktest.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400



def processBooking(booking):
    pid = booking['pid']
    phone = booking['phone']
    test_type = booking['test_type']
    bid = booking['bid']
    bslot = booking['bslot']
    appt = booking['appt']

    location ={
        "consultation": "Room A",
        "xray": "Room B",
        "physiotherapy": "Room C",
        "orthopaedics": "Room D"
    }

    # Invoke the booking microservice --------------------------------------------------
    print('\n-----Invoking booking microservice-----')
    booking_update_URL = "http://127.0.0.1:5000/" + test_type + "/mark_unavailable/" + bid
    booking_update_result = invoke_http(booking_update_URL, method='PUT', json=booking)


    # Check the booking result; if a failure, flag out and return the error.
    code = booking_update_result["code"]
    if code not in range(200, 300):
        return {
            "code": 500,
            "data": {"booking_result": booking_update_result},
            "message": "Internal server error."
        }
    else:
        print("Update booking Status Successful ", booking_update_result)
        print('\n-----Invoking patient microservice-----')
        # print('\n----Update patient appointment time-----')

        # Record in diagnostic test ----------------------------------------------------
        # print('\n\n-----Invoking patient microservice-----')
        # diagnostic_test_URL = "http://127.0.0.1:5050/create_diagnostic_test" 
        # diagnostic_test_result = invoke_http(diagnostic_test_URL, method="POST", json=booking)

        # # Check the order result; if a failure, send it to the error microservice.
        # code = diagnostic_test_result["code"]
        # if code not in range(200, 300):
        #     return {
        #         "code": 500,
        #         "data": {"diagnostic_test_result": diagnostic_test_result},
        #         "message": "Internal server error."
        #     }
        # else:
            # Invoke the notification microservice

        message = "Hi" + pid + ", your appointment at specialist clinic for "+ test_type+" has been booked at " + bslot + " at "+ location[test_type] + ". Please be remineded to bring along your identification documents during registration. Thank You."
        print(message)
#         send_amqp_notification(to_number, message)



# def send_amqp_notification(to_number, message):
#             try:
#                 # Connect to the RabbitMQ server
#                 connection = pika.BlockingConnection(
#                     pika.ConnectionParameters(host='localhost')
#                 )
#                 channel = connection.channel()
#                 # Declare the AMQP queue to send the message
#                 channel.queue_declare(queue='notifications')
#                 # Create the message body as a dictionary
#                 message_body = {'to_number': to_number, 'message': message}
#                 # Publish the message to the queue
#                 channel.basic_publish(
#                     exchange='booking_exchange',
#                     # routing key specify which microservice to call 
#                     routing_key='notification',
#                     body=json.dumps(message_body)
#                 )
#                 # Close the connection to the RabbitMQ server
#                 connection.close()
#                 # Error handling
#             except pika.exceptions.AMQPError as e:
#                 print(f'Error publishing message to AMQP: {str(e)}')
#                 return jsonify(
#                     {
#                         "code": 404,
#                         "message": "Message not sent."
#                     })
#             except Exception as e:
#                 print(f'Error sending notification: {str(e)}')
#                 return jsonify(
#                     {
#                         "code": 404,
#                         "message": "Message not sent."
#                     })
#             else:
#                 print(f'Message sent successfully to {to_number}')
#                 return jsonify({
#                     'code': 200,
#                     'message': 'Message notification is sent to patient'
#                     })


    
#------------------------------------------------------------------------------
# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " making a specialist booking...")
    app.run(host="0.0.0.0", port=5055, debug=True)