import pika
import amqp_setup
import json

# # set up RabbitMQ connection
# connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# channel = connection.channel()

# amqp_setup.check_setup()

# # function to handle incoming messages
# def callback(ch, method, properties, body):
#     data = json.loads(body)
#     # update UI with data from message

# # start consuming messages
# channel.basic_consume(queue='approve_order', on_message_callback=callback, auto_ack=True)
# channel.start_consuming()


# import pika

# Set up connection
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

amqp_setup.check_setup()

# Define callback function to handle incoming messages
def callback(channel, method, properties, body):
    print("Received message:", body)

# Consume message from queue
channel.basic_consume(queue='approve_order', on_message_callback=callback, auto_ack=True)

# Start consuming messages
channel.start_consuming()

