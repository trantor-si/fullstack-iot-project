cd kafka_2.12-2.8.0
bin/kafka-console-consumer.sh --topic $1 --from-beginning --bootstrap-server localhost:9092