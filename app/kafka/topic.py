from kafka.admin import KafkaAdminClient, NewTopic
import os

admin_client = KafkaAdminClient(bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS'))
topic = NewTopic(name=os.getenv('KAFKA_TOPIC_NAME'), num_partitions=int(os.getenv('KAFKA_PARTITIONS')), replication_factor=int(os.getenv('KAFKA_REPLICATION_FACTOR')))
admin_client.create_topics([topic])