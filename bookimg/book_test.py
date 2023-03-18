from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

# make sure the port numbers dont clash
patient_URL = "http://localhost:5004/patient/<int:patient_id>"
consultation_URL = "http://localhost:5000/consultation/unavailable/"
notification_URL = "http://localhost:5002/confirm"


################## make slot unavailable |   access function in booking.py ##############################
# consultation
@app.route("/book_test/consultation/<int:booking_id>", methods=['PUT'])
def processBookTestConsultation(booking_id):

    # 1. Update new booking
    # Invoke the booking microservice
    booking_URL = "http://localhost:5000/consultation/unavailable/" + str(booking_id)
    print('\n\n-----Invoking booking microservice-----')
    booking_status = invoke_http(booking_URL, method="PUT")
    print('booking_result:', booking_status)

    # Check the order result; if a failure, send it to the error microservice.
    # code = booking_status["code"]
    # if code not in range(200, 300):
    # # Inform the notification microservice

    #     # Inform the error microservice
    #     print('\n\n-----Invoking error microservice as booking fails-----')
    #     # invoke_http(error_URL, method="POST", json=booking_status)
    #     # - reply from the invocation is not used; 
    #     # continue even if this invocation fails
    #     print("Booking status ({:d}) sent to the error microservice:".format(code), booking_status)
    #     # Return 
    #     return {
    #             "code": 500,
    #             "data": {"order_result": order_status},
    #             "message": "Booking creation failure sent for error handling."
    #         }

    # WRONG NEED REDO, in AMQP style
    # 2. Invoke noticication microservice upon successful booking
    print('\n\n-----Invoking notification microservice as booking completes-----')
    # invoke_http(notification_URL, method="POST")
    # print("Booking details ({:d}) sent to the notification microservice")
    
    return {
        "message": "alls good no errors here :,)    this is just here so that theres no errors"
    }

# orthopaedics
@app.route("/book_test/orthopaedics/<int:booking_id>", methods=['PUT'])
def processBookTestOrthopaedics(booking_id):

    # 1. Update new booking
    # Invoke the booking microservice
    booking_URL = "http://localhost:5000/orthopaedics/unavailable/" + str(booking_id)
    print('\n\n-----Invoking booking microservice-----')
    booking_status = invoke_http(booking_URL, method="PUT")
    print('booking_result:', booking_status)

    # WRONG NEED REDO, in AMQP style
    # 2. Invoke noticication microservice upon successful booking
    print('\n\n-----Invoking notification microservice as booking completes-----')   
    return {
        "message": "alls good no errors here :,)    this is just here so that theres no errors"
    }

# physiotherapy
@app.route("/book_test/physiotherapy/<int:booking_id>", methods=['PUT'])
def processBookTestPhysiotherapy(booking_id):

    # 1. Update new booking
    # Invoke the booking microservice
    booking_URL = "http://localhost:5000/physiotherapy/unavailable/" + str(booking_id)
    print('\n\n-----Invoking booking microservice-----')
    booking_status = invoke_http(booking_URL, method="PUT")
    print('booking_result:', booking_status)

    # WRONG NEED REDO, in AMQP style
    # 2. Invoke noticication microservice upon successful booking
    print('\n\n-----Invoking notification microservice as booking completes-----')   
    return {
        "message": "alls good no errors here :,)    this is just here so that theres no errors"
    }

# xray
@app.route("/book_test/xray/<int:booking_id>", methods=['PUT', 'POST'])
def processBookTestXray(booking_id):

    # 1. Update new booking
    # Invoke the booking microservice
    booking_URL = "http://localhost:5000/xray/unavailable/" + str(booking_id)
    print('\n\n-----Invoking booking microservice-----')
    booking_status = invoke_http(booking_URL, method="PUT")
    print('booking_result:', booking_status)

    # 1b. Add a new instance to diagnostic_test database
    booking_URL = "http://localhost:5050/create_diagnostic_test/xray"
    print('\n\n-----Invoking patient microservice-----')
    booking_status = invoke_http(booking_URL, method="POST")
    print('diagnostic_test_database_result:', booking_status)
    
    # WRONG NEED REDO, in AMQP style
    # 2. Invoke noticication microservice upon successful booking
    print('\n\n-----Invoking notification microservice as booking completes-----')   
    return {
        "message": "successfully book an appointment and add to the goddamn diagnostic_test database"
    }

###############################################################################################################


################## make slot available |   access function in booking.py ##############################

# consultation
@app.route("/book_test/unbook/consultation/<int:booking_id>", methods=['PUT'])
def UnbookTestConsultation(booking_id):

    # 1. Update new booking
    # Invoke the booking microservice
    booking_URL = "http://localhost:5000/consultation/mark_available/" + str(booking_id)
    print('\n\n-----Invoking booking microservice-----')
    booking_status = invoke_http(booking_URL, method="PUT")
    print('booking_result:', booking_status)

    # WRONG NEED REDO, in AMQP style
    # 2. Invoke noticication microservice upon successful booking
    print('\n\n-----Invoking notification microservice as booking completes-----')   
    return {
        "message": "Session unbooked fk yea"
    }

# orthopaedics
@app.route("/book_test/unbook/orthopaedics/<int:booking_id>", methods=['PUT'])
def UnbookTestOrthopaedics(booking_id):

    # 1. Update new booking
    # Invoke the booking microservice
    booking_URL = "http://localhost:5000/orthopaedics/mark_available/" + str(booking_id)
    print('\n\n-----Invoking booking microservice-----')
    booking_status = invoke_http(booking_URL, method="PUT")
    print('booking_result:', booking_status)

    # WRONG NEED REDO, in AMQP style
    # 2. Invoke noticication microservice upon successful booking
    print('\n\n-----Invoking notification microservice as booking completes-----')   
    return {
        "message": "Session unbooked fk yea"
    }
    
# physiotherapy
@app.route("/book_test/unbook/physiotherapy/<int:booking_id>", methods=['PUT'])
def UnbookTestPhysiotherapy(booking_id):

    # 1. Update new booking
    # Invoke the booking microservice
    booking_URL = "http://localhost:5000/physiotherapy/mark_available/" + str(booking_id)
    print('\n\n-----Invoking booking microservice-----')
    booking_status = invoke_http(booking_URL, method="PUT")
    print('booking_result:', booking_status)

    # WRONG NEED REDO, in AMQP style
    # 2. Invoke noticication microservice upon successful booking
    print('\n\n-----Invoking notification microservice as booking completes-----')   
    return {
        "message": "Session unbooked fk yea"
    }

# xray
@app.route("/book_test/unbook/xray/<int:booking_id>", methods=['PUT'])
def UnbookTestXray(booking_id):

    # 1. Update new booking
    # Invoke the booking microservice
    booking_URL = "http://localhost:5000/xray/mark_available/" + str(booking_id)
    print('\n\n-----Invoking booking microservice-----')
    booking_status = invoke_http(booking_URL, method="PUT")
    print('booking_result:', booking_status)

    # WRONG NEED REDO, in AMQP style
    # 2. Invoke noticication microservice upon successful booking
    print('\n\n-----Invoking notification microservice as booking completes-----')   
    return {
        "message": "Session unbooked fk yea"
    }
#####################################################################################################################


# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
        " making a specialist booking...")
    app.run(host="0.0.0.0", port=5001, debug=True)