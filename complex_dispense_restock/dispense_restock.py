from flask import Flask, request, jsonify
from flask_cors import CORS
from invokes import invoke_http #Used for the invocation of other microservices

import os, sys
import amqp_setup
import pika
import json
import requests

app = Flask(__name__)
CORS(app)

#Routes

#Get Prescriptions
# @app.route("/get_medicines/", methods=['GET'])
# def get_medicines():
#     data = request.get_json()
#     for key,value in data.items():
#         patient_id=key
#         appt_date=value

#     url = f"http://127.0.0.1:5050/check_prescription/{patient_id}/{appt_date}"
#     prescription_results = invoke_http(url, method='GET')
#     ###print (prescription_results)
    
#     if prescription_results['code'] == 250:
#         # Extract the medicine data from the prescription results
#         medicines_data = prescription_results['data']
        
#         # Call the /update_inventory endpoint in inventory.py and pass the medicine data as input
#         inventory_url = f"http://127.0.0.1:5000/update_inventory/"
#         inventory_results = invoke_http(inventory_url, method='PUT', json=medicines_data)
#         ###print(inventory_results)

#         # Send the inventory_results to a queue
#         connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
#         channel = connection.channel()

#         channel.queue_declare(queue='inventory_results')

#         channel.basic_publish(exchange='',
#                             routing_key='inventory_results',
#                             body=str(inventory_results))

#         print("Sent inventory_results to queue")

#         connection.close()
#         ###print('i am printing inventory')
    
#     return prescription_results # will be displayed on UI

@app.route("/get_medicines/", methods=['GET'])
def get_medicines():
    data = request.get_json()
    for key,value in data.items():
        patient_id=key
        appt_date=value

    url = f"http://127.0.0.1:5050/check_prescription/{patient_id}/{appt_date}"
    prescription_results = invoke_http(url, method='GET')
    ###print (prescription_results)
    
    if prescription_results['code'] == 250:
        # Extract the medicine data from the prescription results
        medicines_data = prescription_results['data']
        
        # Call the /update_inventory endpoint in inventory.py and pass the medicine data as input
        inventory_url = f"http://127.0.0.1:5000/update_inventory/"
        inventory_results = invoke_http(inventory_url, method='PUT', json=medicines_data)
        ###print(inventory_results)

        # Send the inventory_results to a queue
        print("=====================================dispense_restock.py - approve order function=====================")

        amqp_setup.check_setup()
        print ('setup')
        # for drug in inventory_results:
        #     for drug_name, topup_amt in drug.items():
        #         print("drug name---",drug_name)
        #         print("top up amount",topup_amt)


        amqp_setup.channel.basic_publish(exchange="approve_order", routing_key="order.exchange", body= inventory_results, properties=pika.BasicProperties(delivery_mode=2))
        print('channel')
    
    return prescription_results # will be displayed on UI

#Send AMQP to UI # invoice only



# #Invoke Patient: Obtain patient prescription data
# @app.route("/get_medicines/<patient_id>/<appt_date>", methods=['GET'])
# def get_medicines(patient_id,appt_date):
#     url = f"http://127.0.0.1:5000/check_prescription/{patient_id}/{appt_date}"
#     results = invoke_http(url, method='GET')
#     print(results)  # Print the results variable
#     return results

# #Invoke Pharmacy: Send patient prescription data, notify to dispense drug
# @app.route("/invoke_pharmacy/<patient_id>/<appt_date>", methods=['PUT'])
# def invoke_pharmacy(patient_id, appt_date):
#     pres_results = get_medicines(patient_id, appt_date)
#     url = f'http://localhost:5201/{appt_date}'
#     response = requests.post(url, json=pres_results)
#     if response.status_code == 200:
#         print('Prescription sent successfully')
#     else:
#         print('Failed to send prescription')


# #Invoke Inventory: Send prescription data to update inventory, receive required restocks if needed
# #Use AMQP: Take in required restocks, send purchase invoice to UI, get approval from UI
# @app.route("/inventory/")
# def update_inventory():
#     url = f"http://127.0.0.1:5000/update_inventory/" 
#     results = invoke_http(url, method='GET')
#     print(results)
#     return results


if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for dispensing medicine...")
    app.run(host="0.0.0.0", port=5203, debug=True)