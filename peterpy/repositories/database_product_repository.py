import logging
from typing import Dict
from uuid import UUID

from peterpy.entities import Product
from peterpy.interfaces import IRepository
from peterpy.libs import match

from peterpy.database.connection import engine

from sqlalchemy import text


class DatabaseProductRepository(IRepository[Product]):
    def get(self, id: UUID) -> Product:
        raise NotImplementedError

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
        raise NotImplementedError

    def remove(self, obj: Product) -> None:
        raise NotImplementedError

    def find(self, query: Dict[str, str]) -> list:
        raise NotImplementedError

    def find_one(self, id: UUID) -> Product:
        raise NotImplementedError

    def all(self) -> list:
        raise NotImplementedError

    def count(self) -> int:
        raise NotImplementedError

    def clear(self) -> None:
        raise NotImplementedError
