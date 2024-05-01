import json
import logging
import uuid
from typing import Dict
from uuid import UUID
from dataclasses import dataclass, field


@dataclass(kw_only=True, frozen=True)
class Product:
    id: UUID = field(default_factory=uuid.uuid4)
    name: str
    price: float

    # overwrites the built-in dunder method
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
