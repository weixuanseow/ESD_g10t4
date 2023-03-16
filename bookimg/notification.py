# pip install twilio
from flask import Flask, request
from twilio.rest import Client
from datetime import datetime, timedelta
import os

app = Flask(__name__)

# Twilio API credentials
account_sid = 'your_account_sid'
auth_token = 'your_auth_token'
client = Client(account_sid, auth_token)

        # let visit_type = sessionStorage.getItem("visit_type")
        # let visit_location = location[visit_type]
        # var location = {
        #   "consulation": "room A",
        #   "xray": "room B",
        #   "physiotherapy": "room C",
        #   "orthopaedics": "room D",
        # }

# To send confirmation messages
@app.route('/confirm', methods=['POST'])
def send_confirmation():
    # Get the booking details from the request
    booking_time = request.json['booking_time']
    user_phone = request.json['user_phone']
    
    # Create and send the confirmation message
    message = client.messages.create(
        body=f"Your booking slot at {booking_time} has been confirmed.",
        from_='YOUR_TWILIO_NUMBER',
        to=user_phone
    )

    return f"Confirmation message sent to {user_phone}."


# We run our application behind an if guard. 
if __name__ == '__main__':
    app.run(port=5000, debug=True)