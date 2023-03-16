from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

# make sure the port numbers dont clash
patient_URL = "http://localhost:5004/patient/<int:patient_id>"
booking_URL = "http://localhost:5000/bookings/unavailable/"
notification_URL = "http://localhost:5002/confirm"


@app.route("/book_test/<int:booking_id>", methods=['PUT'])
def processBookTest(booking_id):

    # 1. Update new booking
    # Invoke the booking microservice
    booking_URL = "http://localhost:5000/bookings/unavailable/" + str(booking_id)
    print('\n\n-----Invoking booking microservice-----')
    booking_status = invoke_http(booking_URL, method="PUT")
    print('booking_result:', booking_status)

    # Check the order result; if a failure, send it to the error microservice.
    code = booking_status["code"]
    if code not in range(200, 300):
    # Inform the notification microservice

        # Inform the error microservice
        print('\n\n-----Invoking error microservice as booking fails-----')
        # invoke_http(error_URL, method="POST", json=booking_status)
        # - reply from the invocation is not used; 
        # continue even if this invocation fails
        print("Booking status ({:d}) sent to the error microservice:".format(code), booking_status)
        # Return 
        return {
                "code": 500,
                "data": {"order_result": order_status},
                "message": "Booking creation failure sent for error handling."
            }

    # WRONG NEED REDO, in AMQP style
    # 2. Invoke noticication microservice upon successful booking
    print('\n\n-----Invoking notification microservice as booking completes-----')
    invoke_http(notification_URL, method="POST")
    print("Booking details ({:d}) sent to the notification microservice")


# def book_test():
#     # Get booking id
#     booking_id = bookings.query.get_or_404(id)

#     # what about patient id , get from session or ?


#     if not booking:
#         return jsonify({'error': 'Booking not found'}), 404


#     # Simple check of input format and data of the request are JSON
#     if request.is_json:
#         try:
#             order = request.get_json()
#             print("\nReceived a booking in JSON:", order)

#             # do the actual work
#             # 1. Send order info {cart items}
#             result = processBookTest(booking_id)
#             return jsonify(result), result["code"]

#         except Exception as e:
#             # Unexpected error in code
#             exc_type, exc_obj, exc_tb = sys.exc_info()
#             fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#             ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
#             print(ex_str)

#             return jsonify({
#                 "code": 500,
#                 "message": "booktest.py internal error: " + ex_str
#             }), 500
#     # if reached here, not a JSON request.
#     return jsonify({
#         "code": 400,
#         "message": "Invalid JSON input: " + str(request.get_data())
#     }), 400

@app.route("/book_test", methods=['GET'])
def process():

    # 1. Update new booking
    # Invoke the booking microservice
    URL = "http://localhost:5000/bookings/all"
    print('\n\n-----Invoking booking microservice TEST TEST TEST-----')
    booking_status = invoke_http(URL, method="GET")
    print('booking_result:', booking_status)

    # Check the order result; if a failure, send it to the error microservice.
    code = booking_status["code"]
    if code not in range(200, 300):
    # Inform the notification microservice

        # Inform the error microservice
        print('\n\n-----Invoking error microservice as booking fails-----')
        # invoke_http(error_URL, method="POST", json=booking_status)
        # - reply from the invocation is not used; 
        # continue even if this invocation fails
        print("Booking status ({:d}) sent to the error microservice:".format(code), booking_status)
        # Return 
        return {
                "code": 500,
                "data": {"order_result": order_status},
                "message": "Booking creation failure sent for error handling."
            }

    # WRONG NEED REDO, in AMQP style
    # 2. Invoke noticication microservice upon successful booking
    print('\n\n-----Invoking notification microservice as booking completes-----')
    invoke_http(notification_URL, method="POST")
    print("Booking details ({:d}) sent to the notification microservice")
    return {
        "code": 201,
        "data": {
            "order_result": "UESSSSSSSSSSSSSSS",
            "shipping_result": "HHHHHHHHHOOOOOOOOOOOOOOOOOOO"
        }
    }




# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
        " making a specialist booking...")
    app.run(host="0.0.0.0", port=5001, debug=True)