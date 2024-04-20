import logging
import json
import uuid
from uuid import UUID
from typing import Dict


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
    def default(self, obj):
        if isinstance(obj, Product):
            return obj.to_json()
        return super().default(obj)
