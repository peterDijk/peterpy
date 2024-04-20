from typing import Dict
from uuid import UUID

from peterpy.entities import Product
from peterpy.interfaces import IRepository


class MemoryProductRepository(IRepository[Product]):
    def __init__(self):
        self.items = {}

    def get(self, id: UUID) -> Product:
        if id not in self.items:
            raise KeyError(f"Product with id {id} not found")
        return self.items[id]

    def add(self, obj: Product) -> None:
        self.items[obj.id] = obj

    def update(self, obj: Product) -> None:
        self.items[obj.id] = obj

    def remove(self, obj: Product) -> None:
        del self.items[obj.id]

    def find(self, query: Dict[str, Product]) -> list:
        return [product for product in self.items.values() if product.name in query]

    def find_one(self, id: UUID) -> Product:
        return self.items[id]

    def all(self) -> list:
        return list(self.items.values())

    def count(self) -> int:
        return len(self.items)

    def clear(self) -> None:
        self.items.clear()
