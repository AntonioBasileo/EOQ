from kafka import KafkaProducer
import json, os

producer = KafkaProducer(
    bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS'),
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    key_serializer=lambda k: k.encode('utf-8'),
    acks=os.getenv('KAFKA_ACKS'),
    retries=int(os.getenv('KAFKA_RETRIES')),
    linger_ms=int(os.getenv('KAFKA_LINGER_MS')),
    compression_type=os.getenv('KAFKA_COMPRESSION_TYPE'),
)

def send(key, value):
    producer.send(
        os.getenv('KAFKA_TOPIC'),
        key=key,
        value=value
    )

    producer.flush()