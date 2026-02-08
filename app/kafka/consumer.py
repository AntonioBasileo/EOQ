from kafka import KafkaConsumer
import json, os

from app.dto.dto import OrderWriteSerializer

consumer = KafkaConsumer(
    os.getenv('KAFKA_TOPIC'),
    bootstrap_servers=[os.environ.get('KAFKA_BOOTSTRAP_SERVERS')],
    group_id=os.getenv('KAFKA_GROUP_ID'),
    auto_offset_reset=os.getenv('KAFKA_AUTO_OFFSET_RESET'),
    enable_auto_commit=os.getenv('KAFKA_ENABLE_AUTO_COMMIT'),
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),
    key_deserializer=lambda k: k.decode('utf-8') if k else None,
    max_poll_records=int(os.getenv('KAFKA_MAX_POLL_RECORDS')),
    consumer_timeout_ms=int(os.getenv('KAFKA_CONSUMER_TIMEOUT_MS')),
)

for msg in consumer:
    serializer = OrderWriteSerializer(data=msg.value)

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(f"Errore durante la deserializzazione del messaggio: {serializer.errors}")

consumer.close()
