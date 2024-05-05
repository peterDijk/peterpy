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
        # self._consumer = AIOKafkaConsumer(
        #     self.topic,
        #     bootstrap_servers=f"localhost:{config["KAFKA_PORT"]}",
        #     group_id="peterpy",
        # )

    # async def start(self):
    #     await self._consumer.start()

    # async def stop(self):
    #     await self._consumer.stop()

    # async def consume(self):
    #     async for msg in self._consumer:
    #         print("consumed: ", msg.topic, msg.partition, msg.offset, msg.key, msg.value)

    async def produce(self, message: str):
        producer = AIOKafkaProducer(
            bootstrap_servers=f"localhost:{config["KAFKA_PORT"]}"
        )

        await producer.start()

        try:
            await producer.send_and_wait(self.topic, kafka_serializer(message), key_serializer("product"))
        finally:
            await producer.stop()
