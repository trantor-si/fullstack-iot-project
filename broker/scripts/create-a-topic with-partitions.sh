cd kafka_2.12-2.8.0
bin/kafka-topics.sh --create --topic $1 --bootstrap-server localhost:9092 --partitions $2