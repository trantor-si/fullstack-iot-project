bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092  --topic $1 --group $2 --reset-offsets --to-earliest --execute
# bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092  --topic bankbranch --group atm-app --reset-offsets --shift-by -2 --execute