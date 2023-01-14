# install kafka-python package
# "pip install kafka-python"

import json
import logging
import random
import time

from confluent_kafka import Producer
from env import EXIT_CODE
from faker import Faker


def get_data_dict():
    data_dict = {}
    fake = Faker()
    
    for i in range(random.randint(10,20)):
        data_dict[i] = {
           'user_id': fake.random_int(min=20000, max=100000),
           'user_name':fake.name(),
           'user_address':fake.street_address() + ' | ' + fake.city() + ' | ' + fake.country_code(),
           'platform': random.choice(['Mobile', 'Laptop', 'Tablet']),
           'signup_at': str(fake.date_time_this_month())    
        }

    return data_dict

def configure ():
    global fake
    fake = Faker()

    logging.basicConfig(format='%(asctime)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename='iot-producer.log',
                        maxBytes=5*1024*1024,
                        backupCount=5,
                        filemode='w')

    global logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

def create_producer(
    server : str = 'localhost:9092', producer_topic : str = 'iot-topic', 
    group_id: str = 'iot-group', kind : str = 'earliest'):
    
    logger.info('Initialization Kafka Producer...')
    global producer
    producer = Producer({'bootstrap.servers': server})
    logger.info('Kafka Producer has been initiated!')

def receipt(err,msg):
    if err is not None:
        print('Error: {}'.format(err))
    else:
        message = 'Produced message on topic {} with value of {}'.format(msg.topic(), msg.value().decode('utf-8'))
        logger.info(message)
        print(message)
        
def run_kafka_producer(
    server : str = 'localhost:9092', producer_topic : str = 'iot-topic', 
    group_id: str = 'iot-group', kind : str = 'earliest', data_dict : dict = {}):
    
    configure()
    create_producer(server, producer_topic, group_id, kind)
    
    # test if data_dict is empty
    if data_dict == {}:
        data_dict = get_data_dict()
    
    for data in data_dict.values():
        print ('\n\n\nData: ', data)
        message=json.dumps(data)
        
        producer.poll(0)
        producer.produce(producer_topic, message.encode('utf-8'), callback=receipt)
        producer.flush()
        
    # producer.produce(producer_topic, EXIT_CODE.encode('utf-8'), callback=receipt)
    # producer.flush()
        
if __name__ == '__main__':
    run_kafka_producer()