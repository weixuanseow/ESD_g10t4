import pika
from os import environ 

hostname = environ.get('rabbit_host') or "localhost" # default hostname
port = environ.get('rabbit_port') or 5672 ###

# connect to the broker and set up a communication channel in the connection
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=hostname, port=port,
        heartbeat=3600, blocked_connection_timeout=3600, # these parameters to prolong the expiration time (in seconds) of the connection
))

channel = connection.channel()

# Find Drug to be restocked (From DispenseAndRestock MS -> Inventory MS)
exchangename="drug_to_restock"
exchangetype="direct"
channel.exchange_declare(exchange=exchangename, exchange_type=exchangetype, durable=True)

############   Approve Order queue   #############
#declare Approve Order queue
queue_name = 'approve_order'
channel.queue_declare(queue=queue_name, durable=True) 
channel.queue_bind(exchange="drug_to_restock", queue="approve_order", routing_key='#') 


def check_setup():
    global connection, channel, hostname, port, exchangename, exchangetype
    if not is_connection_open(connection):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port, heartbeat=3600, blocked_connection_timeout=3600))
    if channel.is_closed:
        channel = connection.channel()
        channel.exchange_declare(exchange=exchangename, exchange_type=exchangetype, durable=True)

def is_connection_open(connection):
    try:
        connection.process_data_events()
        return True
    except pika.exceptions.AMQPError as e:
        print("AMQP Error:", e)
        print("...creating a new connection.")
        return False
