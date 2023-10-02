import pika, json, ssl

credentials = pika.PlainCredentials('staging', 'CAMIlodev1994')

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
parameters = pika.ConnectionParameters(host='b-1ba484aa-4d38-453d-9e5b-bcc42a51aa62.mq.us-east-1.amazonaws.com',
                                       port=5671,
                                       virtual_host='/',
                                       credentials=credentials,
                                       ssl_options=pika.SSLOptions(context)
                                       )

def callback(ch, method, properties, body):
    print('Received in admin')
    data = json.loads(body)
    print(data)


try: 
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='admin')
    channel.confirm_delivery()
    channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

    print('Started Consuming')
    print("Conexión a RabbitMQ establecida con éxito.")
    channel.start_consuming()

    channel.close()

    
except pika.exceptions.AMQPConnectionError as e:
    print("Error de conexión a RabbitMQ:", e)
except Exception as e:
    # Captura y maneja cualquier otra excepción que pueda ocurrir
    print("Error desconocido:", e)







