# install kafka-python package
# "pip install kafka-python"

import json
import logging
import random
import time

from confluent_kafka import Consumer
from env import EXIT_CODE


def configure ():
    logging.basicConfig(format='%(asctime)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename='iot-consumer.log',
                        maxBytes=5*1024*1024,
                        backupCount=5,
                        filemode='w')

    global logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

def create_consumer(
    server : str = 'localhost:9092', consumer_topic : str = 'iot-topic', 
    group_id: str = 'iot-group', kind : str = 'earliest'):
    
    logger.info('Initialization Kafka Consumer...')
    global consumer
    consumer=Consumer(
        {
         'bootstrap.servers': server,
         'group.id': group_id,
         'auto.offset.reset': kind
        }
    )
    logger.info('Kafka Consumer has been initiated!')

    consumer.subscribe([consumer_topic])
    logger.info('Available topics to consume: ', consumer.list_topics().topics)



def run_kafka_consumer(
    server : str = 'localhost:9092', consumer_topic : str = 'iot-topic', 
    group_id: str = 'iot-group', kind : str = 'earliest'):
   
    configure()
    create_consumer(server, consumer_topic, group_id, kind)
    
    while True:
        message = consumer.poll(1.0) #timeout
        if message is None:
            continue
        
        if message.error():
            logger.error('Error: {}'.format(message.error()))
            consumer.close()
            break
        
        data=message.value().decode('utf-8')
        logger.info(data)
        print(data)
        if data == EXIT_CODE:
            consumer.close()
            break
    

if __name__ == '__main__':
    run_kafka_consumer()    