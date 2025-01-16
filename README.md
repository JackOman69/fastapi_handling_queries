# fastapi_handling_queries

 docker exec -it fastapi_handling_queries-kafka-1 echo "/usr/bin/kafka-topics --create --partitions 1 --replication-factor 1 --topic applications --bootstrap-server localhost:9092"

 /usr/bin/kafka-console-consumer --bootstrap-server localhost:9092 --topic applications --from-beginning