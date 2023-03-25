import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='inventory_results')

def callback(ch, method, properties, body):
    # Send the message to the UI via AMQP
    # Replace the `print` statement with your actual code to send the message to the UI
    print("Received inventory_results:", body)

channel.basic_consume(queue='inventory_results', on_message_callback=callback, auto_ack=True)

print('Waiting for inventory_results messages. To exit, press CTRL+C')
channel.start_consuming()