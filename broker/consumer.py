# install kafka-python package
# "pip install kafka-python"

import json
from kafka import KafkaConsumer, KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic, ConfigResource, ConfigResourceType
import uuid

# create KafkaAdminClient - class is to enable fundamental administrative 
# management operations on kafka server such as creating/deleting topic, 
# retrieving, and updating topic configurations and so on.

# 1) bootstrap_servers="localhost:9092" argument specifies the host/IP and port 
# that the consumer should contact to bootstrap initial cluster metadata
# 2) client_id specifies an id of current admin client

admin_client = KafkaAdminClient(bootstrap_servers="localhost:9092", client_id='test')

# Create new topics - Next, the most common usage of admin_client is managing 
# topics such as creating and deleting topics. To create new topics, we first 
# need to define an empty topic list:
topic_list = []

# Then we use the NewTopic class to create a topic with name equals bankbranch,
# partition nums equals to 2, and replication factor equals to 1.
# topicname = uuid.uuid4().__str__()
topicname = "bankbranch"
# new_topic = NewTopic(name=topicname, num_partitions= 2, replication_factor=1)
# topic_list.append(new_topic)

# At last, we can use create_topics(...) method to create new topics:
# equivalent to:
# "kafka-topics.sh --bootstrap-server localhost:9092 --create --topic bankbranch  --partitions 2 --replication_factor 1"
# admin_client.create_topics(new_topics=topic_list)


# Describe a topic - Once new topics are created, we can easily check its 
# configuration details using describe_configs() method
configs = admin_client.describe_configs(
    config_resources=[ConfigResource(ConfigResourceType.TOPIC, topicname)])

# Above describe topic operation is equivalent to using kafka-topics.sh --describe in Kafka CLI client:
# "kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic bankbranch"

# ############################
# PRODUCER
# ############################

# KafkaProducer - Now we have a new bankbranch topic created, we can start 
# produce messages to the topic. For kafka-python, we will use KafkaProducer 
# class to produce messages. Since many real-world message values are in the 
# format of JSON, we will show you how to publish JSON messages as an example.
# First, let’s define and create a KafkaProducer:
producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Since Kafka produces and consumes messages in raw bytes, we need to encode 
# our JSON messages and serialize them into bytes. For the value_serializer 
# argument, we define a lambda function to take a Python dict/list object and
# serialize it into bytes. Then, with the KafkaProducer created, we can use it 
# to produce two ATM transaction messages in JSON format as follows:
producer.send(topicname, {'atmid':29, 'transid':1966})
producer.send(topicname, {'atmid':18, 'transid':1974})

# The first argument specifies the topic bankbranch to be sent, and the second 
# argument represents the message value in a Python dict format and will be 
# serialized into bytes. 

# The above producing message operation is equivalent to using 
# kafka-console-producer.sh --topic in Kafka CLI client:
# "kafka-console-producer.sh --bootstrap-server localhost:9092 --topic bankbranch"



# ############################
# CONSUMER
# ############################

# In the previous step, we published two JSON messages. Now we can use the 
# KafkaConsumer class to consume them. We just need to define and create a 
# KafkaConsumer subscribing to the topic bankbranch:
consumer = KafkaConsumer(topicname, bootstrap_servers=['localhost:9092'], 
    auto_offset_reset='earliest', enable_auto_commit=True, group_id='my-group', 
    value_deserializer=lambda x: json.loads(x.decode('utf-8')))

# Once the consumer is created, it will receive all available messages from 
# the topic bankbranch. Then we can iterate and print them with the following 
# code snippet:
print('Consuming messages from topic {}'.format(topicname))
for msg in consumer:
    print(msg.value)

# for msg in consumer:
#     print(msg.value.decode("utf-8"))

# The above consuming message operation is equivalent to using 
# kafka-console-consumer.sh --topic in Kafka CLI client:
# "kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic bankbranch"