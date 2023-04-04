#pip install twilio
from flask import Flask, request, jsonify
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
# import pika
import os

app = Flask(__name__)

# Define the Twilio account SID and auth token
account_sid = "AC1b140afde89af017b88424de796e6aad"
auth_token = "46481dd25f3f0243f706ceb373189c01"

print("Notification.py is now running------------------")


# Define the client object with the Twilio account SID and auth token
client = Client(account_sid, auth_token)

# Define the route to send a message
@app.route('/send_message', methods=['POST'])
def send_message():
    print("Now calling send_message function------------------")
    try:
        # Get the recipient's phone number and message from the request
        data = request.get_json()
        to_number = data['phone']
        to_number = "+65 9339 8831"
        message = data['message']
        # Use the client object to send a message to the given phone number
        message = client.messages.create(
            to=to_number, # patient number
            from_="+15076657061", # my nummber
            body = message
        )
        print("Message is now sent--------------------------------")
        # Return the message SID
        return jsonify({
            "code": 200,
            'message_sid': message.sid
            })
    except TwilioRestException as e:
        print(f"Error sending message to {to_number}: {str(e)}")
        return jsonify(
        {
            "code": 404,
            "message": "Message failed to send ."
        }
    ), 404



# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " sending message to patient.")
    app.run(host="0.0.0.0", port=5008, debug=True)