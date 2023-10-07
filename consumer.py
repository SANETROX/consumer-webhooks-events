import pika, json, ssl, sys
import pymongo
from pymongo import MongoClient

try:
    mongo_client = MongoClient('mongodb://mongo:tBhJm2OF7QtOPG5zND34@containers-us-west-119.railway.app:5610')
    db = mongo_client['events_webhooks']

    print('Conexión establecida con MongoDB')
except ConnectionError as e:
    # Si ocurre un error de conexión, imprime un mensaje de error y el tipo de error
    print('Error de conexión a MongoDB:', e.args)
except Exception as e:
    # Captura y maneja cualquier otro error que pueda ocurrir
    print('Error desconocido:', e.args)

credentials = pika.PlainCredentials('staging', 'CAMIlodev1994')

context = ssl.create_default_context()
parameters = pika.ConnectionParameters(host='b-1ba484aa-4d38-453d-9e5b-bcc42a51aa62.mq.us-east-1.amazonaws.com',
                                       port=5671,
                                       virtual_host='/',
                                       credentials=credentials,
                                       ssl_options=pika.SSLOptions(context)
                                       )

def callback(ch, method, properties, body):
    print('Received in admin')
    sys.stdout.flush()
    collection = db['events']
    data = json.loads(body)
    data['idOrder'] = data.pop('_id')
    collection.insert_one(data)
    print(data)
    sys.stdout.flush()


try: 
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='admin')
    channel.confirm_delivery()
    channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

    print('Started Consuming')
    print("Conexión a RabbitMQ establecida con éxito.")
    sys.stdout.flush()
    channel.start_consuming()

    channel.close()

    
except pika.exceptions.AMQPConnectionError as e:
    print("Error de conexión a RabbitMQ:", e)
    sys.stdout.flush()
except Exception as e:
    # Captura y maneja cualquier otra excepción que pueda ocurrir
    print("Error desconocido:", e)
    sys.stdout.flush()







