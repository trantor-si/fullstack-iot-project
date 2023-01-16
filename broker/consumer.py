# install kafka-python package
# "pip install kafka-python"

import json
import logging
import random
import time

from confluent_kafka import Consumer
from env import EXIT_CODE


def create_logger (filename: str = 'iot-consumer.log', silent: bool = False):
    logging.basicConfig(format='%(asctime)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename=filename,
                        filemode='w')

    global logger
    global silent_logger
    silent_logger = silent
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    log ('Logger [{}] has been initiated!'.format(filename))

def log (message, type = 'info'):
    if type == 'error':
        logger.error(message)
        if (not silent_logger): print ('Error: {}'.format(message))
    else:
        logger.info(message)
        if (not silent_logger): print ('Info: {}'.format(message))

def create_consumer(server, consumer_topic, group_id, offset):
    log('Initialization Kafka Consumer...')
    consumer=Consumer(
        {
         'bootstrap.servers': server,
         'group.id': group_id,
         'auto.offset.reset': offset
        }
    )
    log('Kafka Consumer has been initiated!')

    consumer.subscribe([consumer_topic])
    log('Topic to consume: [{}]', consumer_topic)
    
    return consumer

def run_kafka_consumer(
    server : str = 'localhost:9092', consumer_topic : str = 'iot-topic', 
    group_id: str = 'iot-group', offset : str = 'earliest', silent : bool = False):
   
    create_logger(silent=silent)
    consumer = create_consumer(server, consumer_topic, group_id, offset='latest')
    
    timestamp = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    result_dict = {timestamp: []}
    log('Consumer Execution started! Result dictionary has been initiated: [{}] at [{}]'.format(result_dict, timestamp))
    
    while True:
        message = consumer.poll(0.1) #timeout
        if message is None:
            continue
        
        if message.error():
            log('{}. Execution terminated!'.format(message.error()), 'error')
            consumer.close()
            return None
        
        message_value = message.value().decode('utf-8')
        if str(message_value).find(EXIT_CODE) != -1:
            log('Exit code received. Consumer Execution terminated!')
            consumer.close()

            log('\n\n\nFINAL RESULT:\n{}\n\n\n'.format(result_dict))
            return result_dict
        else:
            data = json.loads(message_value)
            
            # append data to result_dict
            result_dict[timestamp].append(data)
            log('Consumed message on topic [{}] with value of [{}] and type [{}]'.format(message.topic(), data, type(data)))
            continue

if __name__ == '__main__':
    run_kafka_consumer()    