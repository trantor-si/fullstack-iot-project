cd kafka_2.12-2.8.0
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic $1 --group $2