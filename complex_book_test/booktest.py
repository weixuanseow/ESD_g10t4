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
    url_str = os.environ.get('bookingURL') or 'http://127.0.0.1:5000/'
    booking_update_URL = url_str + test_type + "/mark_unavailable/" + bid
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
        url_str = os.environ.get('patientURL') or 'http://127.0.0.1:5051/'
        diagnostic_test_URL = f"{url_str}create_diagnostic_test" 
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
            message = "Please be reminded of your " + test_type.upper()  + " test at " + location[test_type] + " at " + bslot + ". Please bring the required documents during your visit. Thank you."
            booking['message'] = message
            print(booking)
            url_str = os.environ.get('notificationURL') or 'http://127.0.0.1:5008/'
            notification_URL = f"{url_str}send_message" 
            notification_result = invoke_http(notification_URL, method="POST", json=booking)
            code = notification_result["code"]
            if code not in range(200, 300):
                return jsonify({
                        'code': 500,
                        'message': 'Internal error - notification '
                    })
            else:
                return jsonify({
                        'code': 200,
                        'message': '================ BookTest Complex microservice Done ================'
                    })


#------------------------------------------------------------------------------
# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " making a specialist booking...")
    app.run(host="0.0.0.0", port=5055, debug=True)