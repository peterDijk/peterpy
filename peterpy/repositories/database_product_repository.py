import logging
from typing import Dict
from uuid import UUID

from peterpy.entities import Product
from peterpy.interfaces import IRepository
from peterpy.libs import match

from peterpy.database.connection import engine

from sqlalchemy import text


class DatabaseProductRepository(IRepository[Product]):
    def __init__(self):
        self.items = {}

    def get(self, id: UUID) -> Product:
        if id not in self.items:
            raise KeyError(f"Product with id {id} not found")
        return self.items[id]

    def add(self, obj: Product) -> None:
        with engine.connect() as connection:
            connection.execute(
                text("INSERT INTO example (name) VALUES (:name)"), {"name": obj.name}
            )
            # connection.execute(
            #     text("INSERT INTO example (name) VALUES (:name)"),
            #     [{"name": "Barry"}, {"name": "Christina"}],
            # )
            connection.commit()
        # self.items[obj.id] = obj

    def update(self, obj: Product) -> None:
        self.items[obj.id] = obj

    def remove(self, obj: Product) -> None:
        del self.items[obj.id]

    def find(self, query: Dict[str, str]) -> list:
        results = [product for product in self.items.values() if match(product, query)]

        logging.debug(f"Found {len(results)} products with query {query}")

        return results

    def find_one(self, id: UUID) -> Product:
        return self.items[id]

    def all(self) -> list:
        return list(self.items.values())

    def count(self) -> int:
        return len(self.items)

    def clear(self) -> None:
        self.items.clear()