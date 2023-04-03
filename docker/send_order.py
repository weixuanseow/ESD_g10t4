import pika
import amqp_setup
import requests

# Set up connection
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

amqp_setup.check_setup()

# handle incoming messages
def callback(channel, method, properties, body):
    print("Received message:", body)

    # Send message to microservice
    url = 'http://127.0.0.1:5204/receive_message'
    data = {'message': body.decode('utf-8')}
    requests.post(url, json=data)

# Consume message from queue
channel.basic_consume(queue='approve_order', on_message_callback=callback, auto_ack=True)

# Start consuming messages
channel.start_consuming()
