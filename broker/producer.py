# install kafka-python package
# "pip install kafka-python"

import json
import logging
import random
import time
from uuid import uuid4

from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer
from env import EXIT_CODE, EXIT_CODE_DICT
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

def create_logger (filename: str = 'iot-producer.log'):
    logging.basicConfig(format='%(asctime)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename=filename,
                        filemode='w')

    global logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    log ('Logger [{}] has been initiated!'.format(filename))

def log (message, type = 'info'):
    if type == 'error':
        logger.error(message)
        print ('Error: {}'.format(message))
    else:
        logger.info(message)
        print ('Info: {}'.format(message))

def create_producer(
    server : str = 'localhost:9092', producer_topic : str = 'iot-topic', 
    group_id: str = 'iot-group', kind : str = 'earliest'):
    
    log('Initialization Kafka Producer...')
    producer = Producer({'bootstrap.servers': server})
    log('Kafka Producer has been initiated!')
    return producer

def receipt(err,msg):
    if err is not None:
        log('{}'.format(err), 'error')
    else:
        message = 'Produced message on topic [{}] with value of [{}] and type [{}]'.format(msg.topic(), msg.value().decode('utf-8'),type(msg))
        log(message)
        
def delivery_report(err, msg):
    """
    Reports the success or failure of a message delivery.
    Args:
        err (KafkaError): The error that occurred on None on success.
        msg (Message): The message that was produced or failed.
    """

    if err is not None:
        log("Delivery failed for User record [{}]: [{}]".format(msg.key(), err), 'error')
        return
    
    log('User record [{}] successfully produced to topic [{}], partition [{}], at offset [{}]'.format(
        msg.key(), msg.topic(), msg.partition(), msg.offset()))

def send_a_message(data, producer, string_serializer, producer_topic):
    producer.poll(0)
    message=json.dumps(data)
    producer.produce(
        topic=producer_topic, 
        key=string_serializer(str(uuid4()), None),
        value=message, 
        callback=delivery_report)
    producer.flush()

def run_kafka_producer(
    server : str = 'localhost:9092', producer_topic : str = 'iot-topic', 
    group_id: str = 'iot-group', kind : str = 'earliest', data_dict : dict = {}):
    
    create_logger()
    producer = create_producer(server, producer_topic, group_id, kind)
    
    # test if data_dict is empty
    if data_dict == {}:
        data_dict = get_data_dict()
    
    string_serializer = StringSerializer('utf_8')
    for data in data_dict.values():
        send_a_message(data, producer, string_serializer, producer_topic)

    # send exit code
    send_a_message(json.dumps(EXIT_CODE), producer, string_serializer, producer_topic)

    log('Producer has been successfuly closed!')
        
if __name__ == '__main__':
    run_kafka_producer()