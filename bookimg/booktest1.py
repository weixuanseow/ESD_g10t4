from flask import Flask, request, jsonify
from flask_cors import CORS
from invokes import invoke_http


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
    visit_type = booking['visit_type']
    bid = booking['bid']

    # Invoke the booking microservice --------------------------------------------------
    print('\n-----Invoking booking microservice-----')
    booking_update_URL = "http://127.0.0.1:5000/" + visit_type + "/mark_unavailable/" + bid
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
        # else:
            # Invoke the notification microservice
            # send_confirmation(phone,booking)
            # def send_confirmation(phone_number, booking_details):
            #     connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            #     channel = connection.channel()
            #     channel.queue_declare(queue='booking_confirmation')

            #     message = {'phone_number': phone_number, 'booking_details': booking_details}
            #     channel.basic_publish(exchange='', routing_key='booking_confirmation', body=json.dumps(message))


            #     # invoke notification through AMQP ----------------------------------------------------
            #     # message = json.dumps(booking)
            #     # amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="order.error", 
            #     # body=message, properties=pika.BasicProperties(delivery_mode = 2)) 


            # connection.close()
            

    
#------------------------------------------------------------------------------
# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " making a specialist booking...")
    app.run(host="0.0.0.0", port=5050, debug=True)