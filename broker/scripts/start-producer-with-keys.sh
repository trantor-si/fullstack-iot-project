cd kafka_2.12-2.8.0
clear && bin/kafka-console-producer.sh --bootstrap-server localhost:9092 --topic $1 --property parse.key=true --property key.separator=: