import json

from peterpy.config import config

# mypy: ignore-errors
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

def kafka_serializer(value):
    return json.dumps(value).encode()


def key_serializer(value):
    return json.dumps(value).encode()


def encode_json(msg):
    to_load = msg.value.decode("utf-8")
    return json.loads(to_load)


class KafkaService:
    def __init__(self, topic: str):
        self.topic = topic

    async def start(self):
        self._consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=f"{config["KAFKA_HOST"]}:{config["KAFKA_PORT"]}",
            group_id="peterpy",
        )    
            
        await self._consumer.start()

    async def stop(self):
        await self._consumer.stop()

    async def consume(self):
        async for msg in self._consumer:
            print("consumed: ", msg.topic, msg.partition, msg.offset, msg.key, msg.value)

    async def produce(self, message: dict[str, str]):
        producer = AIOKafkaProducer(
            bootstrap_servers=f"{config["KAFKA_HOST"]}:{config["KAFKA_PORT"]}"
        )

        await producer.start()

        try:
            ready_message = kafka_serializer(message)
            topic = kafka_serializer(self.topic)
            await producer.send_and_wait(self.topic, ready_message, topic)
        finally:
            await producer.stop()
