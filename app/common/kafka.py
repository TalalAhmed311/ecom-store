import asyncio
import json
from typing import Any
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from app.common.config import settings

class KafkaProducer:
    def __init__(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    async def start(self):
        await self.producer.start()

    async def stop(self):
        await self.producer.stop()

    async def send(self, topic: str, value: Any):
        try:
            await self.producer.send_and_wait(topic, value)
        except Exception as e:
            print(f"Failed to send message to Kafka: {e}")
            # Depending on requirements, re-raise or log.

kafka_producer = KafkaProducer()

def get_kafka_producer():
    return kafka_producer
