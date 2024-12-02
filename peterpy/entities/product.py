import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from uuid import UUID

from peterpy.interfaces.entity import IEntity


@dataclass(kw_only=True, frozen=True)
class Product(IEntity):
    product_id: UUID = field(default_factory=uuid.uuid4)
    name: str
    price: float
    date_added: Optional[str] = None

    def to_json(self) -> Dict[str, Any]:
        return {
            "product_id": str(self.product_id),
            "name": self.name,
            "price": self.price,
            "date_added": self.date_added,
        }
