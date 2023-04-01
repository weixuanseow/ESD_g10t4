from flask import Flask, request, jsonify
from flask_cors import CORS
from invokes import invoke_http #Used for the invocation of other microservices
from flask_socketio import SocketIO

import os, sys
import amqp_setup
import pika
import json
import requests
import pickle

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

#Routes

@app.route("/get_medicines/<patient_id>/<appt_date>", methods=['GET'])
def get_medicines(patient_id, appt_date):

    url = f"http://127.0.0.1:5051/check_prescription/{patient_id}/{appt_date}"
    prescription_results = invoke_http(url, method='GET')
    ###print (prescription_results)
    
    if prescription_results['code'] == 250:
        # Extract the medicine data from the prescription results
        medicines_data = prescription_results['data']
        new_data = {}
        for key, value in medicines_data.items():
            new_data[key] = int(value[0][0])

        # Call the /update_inventory endpoint in inventory.py and pass the medicine data as input
        inventory_url = f"http://127.0.0.1:5211/update_inventory"
        inventory_results = invoke_http(inventory_url, method='PUT', json=new_data)
        print(inventory_results)
        print (type(inventory_results))

        # Send the inventory_results to a queue
        print("=====================================dispense_restock.py - approve order function=====================")

        amqp_setup.check_setup()

        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        channel.basic_publish(exchange='drug_to_restock',
                            routing_key='#',
                            body= "Draft Order: " + str(inventory_results['data']),
                            properties=pika.BasicProperties(
                                delivery_mode = 2 # make message persistent
                            ))


        connection.close()

    
    return prescription_results # will be displayed on UI
    
@app.route('/receive_message', methods=['POST'])
def receive_message():
    message = request.json.get('message')
    print("Received message:", message)
    if message:
        # Emit the message as an event to all connected clients
        socketio.emit('top_up_message', message, namespace='/')
        return 'OK', 200
    else:
        return 'Bad Request', 400


if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for dispensing medicine...")
    app.run(host="0.0.0.0", port=5204, debug=True)