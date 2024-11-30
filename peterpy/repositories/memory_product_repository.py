import logging
from typing import Dict, Generator
from uuid import UUID

from peterpy.entities import Product
from peterpy.interfaces import IRepository
from peterpy.libs import match


class MemoryProductRepository(IRepository[Product]):
    def __init__(self):
        self.items = {}

    def get(self, product_id: UUID) -> Product:
        if product_id not in self.items:
            raise KeyError(f"Product with product_id {product_id} not found")
        return self.items[product_id]

    def add(self, obj: Product, flush=False) -> Product:
        self.items[obj.product_id] = obj

        return obj

    def update(self, obj: Product) -> Product:
        self.items[obj.product_id] = obj

        return obj

    def remove(self, obj: Product) -> Product:
        del self.items[obj.product_id]

        return obj

    def find(self, query: Dict[str, str]) -> list:
        results = [product for product in self.items.values() if match(product, query)]

        logging.debug("Found %s products with query %s", len(results), query)

        return results

    def find_one(self, obj_id: UUID) -> Product:
        return self.items[obj_id]

    def all(self) -> Generator[Product, None, None]:
        # for product in self.items.values():
        #     yield product
        yield from self.items.values()

    def count(self) -> int:
        return len(self.items)

    def clear(self) -> None:
        self.items.clear()
