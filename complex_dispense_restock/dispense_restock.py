from flask import Flask, request, jsonify
from flask_cors import CORS
from invokes import invoke_http #Used for the invocation of other microservices

import os, sys
import amqp_setup
import pika ##MINNAL: Why is this underlined omg...
import json
import requests ##MINNAL: If needed ya.. i j put first...

app = Flask(__name__)
CORS(app)

#maybe the URLs can be defined inside the function like whats in the Invoke Patient route? then the variables easier? idk...
pharmacy_URL = "http://localhost:5201/pharmacy/<string:appt_datetime>" 
inventory_URL = "http://localhost:5200/inventory/create_order" #Jayme: is it i get my data from inventory through routing 
order_URL = "http://localhost:5000/inventory" # (????????) 

#Routes

#Invoke Patient: Obtain patient prescription data
@app.route("/get_medicines/<patient_id>/<appt_date>", methods=['GET'])
def get_medicines(patient_id,appt_date):
    url = f"http://127.0.0.1:5000/check_prescription/{patient_id}/{appt_date}"
    results = invoke_http(url, method='GET')
    print(results)  # Print the results variable
    return results
#but aft this i am truly lost i need to see the UI cos idk what im doing alr...

#Invoke Pharmacy: Send patient prescription data, notify to dispense drug
@app.route("/invoke_pharmacy/<patient_id>/<appt_date>", methods=['PUT'])
def invoke_pharmacy(patient_id, appt_date):
    pres_results = get_medicines(patient_id, appt_date)
    url = f'http://localhost:5201/{appt_date}'
    response = requests.post(url, json=pres_results)
    if response.status_code == 200:
        print('Prescription sent successfully')
    else:
        print('Failed to send prescription')


#Invoke Inventory: Send prescription data to update inventory, receive required restocks if needed
@app.route("/inventory/")
def update_inventory():
    url = f"http://127.0.0.1:5000/update_inventory/" 
    results = invoke_http(url, method='GET')
    print(results)
    return results

#Use AMQP: Take in required restocks, send purchase invoice to UI, get approval from UI

# dispense medicine

# create draft purchase to order new stock when stock < threshold amount
# get data from inventory, order should have drug name and top up amount
@app.route("/create_order/<drug_full_name>",methods=['POST'])
def create_order():
    if request.is_json:
        try:
            order = request.get_json() # how to get request?
            print("\nReceived an order in JSON:", order)

            # do the actual work
            # 1. Send order info {cart items}
            result = processPlaceOrder(order)
            print('\n------------------------')
            print('\nresult: ', result)
            return jsonify({
                "code": result["code"],
                "data": result
                })

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "place_order.py internal error: " + ex_str
            }), 500
        
    # order = []
    # drug_full_name = Inventory.query.filter_by(drug_full_name=drug_full_name)
    # if drug_full_name.current_amt<=drug_full_name.threshold_amt:
    #     order.append((drug_full_name, drug_full_name.topup_amt))
        
def processPlaceOrder(order):
    # 2. Send the order info {cart items}
    # Invoke the order microservice
    print('\n-----Invoking order microservice-----')
    order_result = invoke_http(order_URL, method='POST', json=order)
    print('order_result:', order_result)
  
    # Check the order result; if a failure, send it to the error microservice.
    code = order_result["code"]
    message = json.dumps(order_result)

    amqp_setup.check_setup()

    if code not in range(200, 300):
        # Inform the error microservice
        #print('\n\n-----Invoking error microservice as order fails-----')
        print('\n\n-----Publishing the (order error) message with routing_key=order.error-----')

        # invoke_http(error_URL, method="POST", json=order_result)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="order.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        # make message persistent within the matching queues until it is received by some receiver 
        # (the matching queues have to exist and be durable and bound to the exchange)

        # - reply from the invocation is not used;
        # continue even if this invocation fails        
        print("\nOrder status ({:d}) published to the RabbitMQ Exchange:".format(
            code), order_result)

        # 7. Return error
        return {
            "code": 500,
            "data": {"order_result": order_result},
            "message": "Order creation failure sent for error handling."
        }

    # Notice that we are publishing to "Activity Log" only when there is no error in order creation.
    # In http version, we first invoked "Activity Log" and then checked for error.
    # Since the "Activity Log" binds to the queue using '#' => any routing_key would be matched 
    # and a message sent to “Error” queue can be received by “Activity Log” too.

    else:
        # 4. Record new order
        # record the activity log anyway
        #print('\n\n-----Invoking activity_log microservice-----')
        print('\n\n-----Publishing the (order info) message with routing_key=order.info-----')        

        # invoke_http(activity_log_URL, method="POST", json=order_result)            
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="order.info", 
            body=message)
    
    print("\nOrder published to RabbitMQ Exchange.\n")
    # - reply from the invocation is not used;
    # continue even if this invocation fails
    
    # 5. Send new order to shipping
    # Invoke the shipping record microservice
    print('\n\n-----Invoking shipping_record microservice-----')    
    
    order_result = invoke_http(
        inventory_URL, method="POST", json=order_result['data'])
    print("shipping_result:", shipping_result, '\n') ##MINNAL: Define shipping_result?

    # Check the shipping result;
    # if a failure, send it to the error microservice.
    code = shipping_result["code"]
    if code not in range(200, 300):
        # Inform the error microservice
        #print('\n\n-----Invoking error microservice as shipping fails-----')
        print('\n\n-----Publishing the (shipping error) message with routing_key=shipping.error-----')

        # invoke_http(error_URL, method="POST", json=shipping_result)
        message = json.dumps(shipping_result)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="shipping.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2))

        print("\nShipping status ({:d}) published to the RabbitMQ Exchange:".format(
            code), shipping_result)

        # 7. Return error
        return {
            "code": 400,
            "data": {
                "order_result": order_result,
                "shipping_result": shipping_result
            },
            "message": "Simulated shipping record error sent for error handling."
        }

    # 7. Return created order, shipping record
    return {
        "code": 201,
        "data": {
            "order_result": order_result,
            "shipping_result": shipping_result
        }
    }

# notify registrar to approve draft order
# part with fire and forget, uses the same data from create order
@app.route("/approve_order",methods=['GET'])
def approve_order():
    print("======================================prepare_order.py - approve order function=====================")

    amqp_setup.check_setup()
    drug_name = request.json.get('payment_url', None)
    topup_amt = request.json.get('customer_email', None)
    
    print("drug name---",drug_name)
    print("top up amount",topup_amt)

    #Invoke inventory MS to retrieve drug topup details
    msg_content = json.dumps({
        "customer_details":
            {
            "customer_name": customer_name, 
            "customer_email": customer_email,
            "payment_link": payment_link
            }
    })

    amqp_setup.channel.basic_publish(exchange="approve_order", routing_key="order.exchange", body= msg_content, properties=pika.BasicProperties(delivery_mode=2))
    return jsonify({
        "code": 201,
        "message": "Payment Email Sent Successfully"
        }
    ), 201

if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for placing an order...")
    app.run(host="0.0.0.0", port=5202, debug=True)