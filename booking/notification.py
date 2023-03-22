# pip install twilio
from flask import Flask, request
from twilio.rest import Client
from datetime import datetime, timedelta
import os

import pika
import json


def callback(ch, method, properties, body):
    message = json.loads(body.decode('utf-8'))
    phone_number = message['phone_number']
    booking_details = message['booking_details']

    # Send confirmation message using Twilio API
    account_sid = 'YOUR_ACCOUNT_SID'
    auth_token = 'YOUR_AUTH_TOKEN'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f"Your booking is confirmed for {booking_details}.",
        from_='+1234567890',
        to=phone_number
    )

    print(f"Sent confirmation message to {phone_number}: {message.sid}")

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='booking_confirmation')
channel.basic_consume(queue='booking_confirmation', on_message_callback=callback, auto_ack=True)

print('Waiting for confirmation messages...')
channel.start_consuming()

# We run our application behind an if guard. 
if __name__ == '__main__':
    app.run(port=5009, debug=True)