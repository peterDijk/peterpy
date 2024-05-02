import json
import uuid
from dataclasses import dataclass, field
from uuid import UUID


@dataclass(kw_only=True, frozen=True)
class Product:
    product_id: UUID = field(default_factory=uuid.uuid4)
    name: str
    price: float

    def to_json(self):
        return {
            "product_id": str(self.product_id),
            "name": self.name,
            "price": self.price,
        }


class ProductEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Product):
            return o.to_json()
        return super().default(o)
