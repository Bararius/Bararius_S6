import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()


channel.queue_declare(queue='localhost')

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')


connection.close()