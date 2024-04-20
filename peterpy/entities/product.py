import json
import uuid
from uuid import UUID


class Product:
    id: UUID
    name: str
    price: float

    def __init__(self, name: str, price: float):
        self.id = uuid.uuid4()
        self.name = name
        self.price = price

    def update_name(self, name: str):
        self.name = name

    def update_price(self, price: float):
        self.price = price

    def __str__(self):
        return f"{self.name} - ${self.price}"

    def to_json(self):
        return {
            "id": self.id.__str__(),
            "name": self.name,
            "price": self.price,
        }


class ProductEncoder(json.JSONEncoder):
    def default(self, obj: Product):
        if isinstance(obj, Product):
            return obj.to_json()

            # grey because in typing i'm already saying that obj is a Product. BUT python doesn't enforce typing at runtime so this is a good practice ?
        return super().default(obj)
