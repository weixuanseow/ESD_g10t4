from flask import Flask, request, jsonify
from flask_cors import CORS
from invokes import invoke_http
from twilio.rest import Client

import os, sys
import requests

# import amqp_setup
# import pika
import json

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
            print(result)
            return result

        except Exception as e:
            # Unexpected error in code
            print('HELLO ERROR')
            # exc_type, exc_obj, exc_tb = sys.exc_info()
            # # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # # ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            # # print(ex_str)
            # print(exc_type)
            # print(exc_tb)

            return jsonify({
                "code": 500,
                "message": "booktest.py internal error: " 
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400



def processBooking(booking):
    pid = booking['pid']
    to_number = booking['phone']
    test_type = booking['test_type']
    bid = booking['bid']
    bslot = booking['bslot']
    appt = booking['appt']

    location ={
        "mri": "Room A",
        "xray": "Room B",
        "ctscan": "Room C",
        "bloodtest": "Room D"
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
        print('\n----Update patient appointment time-----')

        # Record in diagnostic test ----------------------------------------------------
        print('\n\n-----Invoking patient microservice-----')
        diagnostic_test_URL = "http://127.0.0.1:5050/create_diagnostic_test" 
        diagnostic_test_result = invoke_http(diagnostic_test_URL, method="POST", json=booking)


        # Check the order result; if a failure, send it to the error microservice.
        code = diagnostic_test_result["code"]
        if code not in range(200, 300):
            return {
                "code": 500,
                "data": {"diagnostic_test_result": diagnostic_test_result},
                "message": "Internal server error."
            }
        else:
            print('\n\n-----Invoking notification microservice-----')
            message = "Please be reminded of your booked test at " + location[test_type] + " at " + bslot
            booking['message'] = message
            print(booking)
            # Invoke the notification microservice
            # import json
            # import pika
            # from notification import send_message

            # def receive_message():
            #     try:
            #         # Connect to the RabbitMQ server
            #         connection = pika.BlockingConnection(
            #             pika.ConnectionParameters(host='localhost')
            #         )
            #         channel = connection.channel()
            #         # Declare the exchange to consume messages from
            #         channel.exchange_declare(exchange='booking_exchange', exchange_type='direct')
            #         # Declare the queue to consume messages from
            #         channel.queue_declare(queue='notifications', durable=True)
            #         # Bind the queue to the exchange with the routing key
            #         channel.queue_bind(exchange='booking_exchange', queue='notifications', routing_key='notification')
            #         # Define the callback function to invoke when a message is received
            #         def callback(ch, method, properties, body):
            #             # Parse the message body as a dictionary
            #             message_body = json.loads(body)
            #             # Extract the to_number and message from the message body
            #             to_number = message_body.get('to_number')
            #             message = message_body.get('message')
            #             # Call the send_message function with the extracted data
            #             send_message(to_number, message)
            #             # Acknowledge the message to RabbitMQ
            #             ch.basic_ack(delivery_tag=method.delivery_tag)
            #         # Consume messages from the queue with the callback function
            #         channel.basic_qos(prefetch_count=1)
            #         channel.basic_consume(queue='notifications', on_message_callback=callback)
            #         print(' [*] Waiting for messages. To exit press CTRL+C')
            #         channel.start_consuming()
            #         # Close the connection to the RabbitMQ server
            #         connection.close()
            #         return jsonify({
            #             'code': 200,
            #             'message': 'Complex microservice done'
            #             })
            #     except pika.exceptions.AMQPError as e:
            #         print(f'Error consuming message from AMQP: {str(e)}')
            #     except Exception as e:
            #         print(f'Error receiving message: {str(e)}')
            # receive_message()
            notification_URL = "http://127.0.0.1:5008/send_message" 
            notification_result = invoke_http(notification_URL, method="POST", json=booking)
            code = notification_result["code"]
            if code not in range(200, 300):
                return jsonify({
                        'code': 500,
                        'message': 'Internal error - notifcation '
                    })
            else:
                return jsonify({
                        'code': 200,
                        'message': 'Complex microservice done'
                    })








    
#------------------------------------------------------------------------------
# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " making a specialist booking...")
    app.run(host="0.0.0.0", port=5055, debug=True)