from kafka import KafkaConsumer
import cdc_load_sql as c
import json

def cdc_consume():
    KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
    KAFKA_TOPIC_MONGO_CDC = "mongo-cdc"
    KAFKA_CONSUMER_GROUP_ID = "mongo_cdc_db"

    consumer = KafkaConsumer(
        KAFKA_TOPIC_MONGO_CDC,
        bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id=KAFKA_CONSUMER_GROUP_ID
    )

    print(f"Listening for messages on topic: {KAFKA_TOPIC_MONGO_CDC}...")
    try:
        for message in consumer:
            try:
                print(f"Received message: {message.value}")
                c.cdc_db_insert(message.value)
            except Exception as e:
                print(f"Failed to process message: {e}")
                print(f"Skipping message: {message.value}")
                continue  # move to next message
    except Exception as e:
        print(f"Error connecting or loading data: {e}")
    finally:
        consumer.close()  # Ensure proper resource release
