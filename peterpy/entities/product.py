import json
from typing import Any, Dict
import uuid
from dataclasses import dataclass, field
from uuid import UUID

from peterpy.interfaces.entity import IEntity


@dataclass(kw_only=True, frozen=True)
class Product(IEntity):
    product_id: UUID = field(default_factory=uuid.uuid4)
    name: str
    price: float

    # def __str__(self) -> str:
    # return {
    #     "product_id": str(self.product_id),
    #     "name": self.name,
    #     "price": self.price,
    # }

    def to_json(self) -> Dict[str, Any]:
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
