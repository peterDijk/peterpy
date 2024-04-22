import logging
from typing import Dict
from uuid import UUID

from peterpy.entities import Product
from peterpy.interfaces import IRepository
from peterpy.libs import match

from peterpy.database.connection import engine

from sqlalchemy import text
from sqlalchemy.orm import Session

from peterpy.database.data_mapper import (
    product_model_to_entity,
    product_entity_to_model,
)


class DatabaseProductRepository(IRepository[Product]):
    def get(self, id: UUID) -> Product:
        raise NotImplementedError

    def add(self, obj: Product) -> None:
        instance = product_entity_to_model(obj)
        with Session(engine) as session:
            session.add(instance)
            session.commit()

    def update(self, obj: Product) -> None:
        raise NotImplementedError

    def remove(self, obj: Product) -> None:
        raise NotImplementedError

    def find(self, query: Dict[str, str]) -> list:
        return []
        # raise NotImplementedError

    def find_one(self, id: UUID) -> Product:
        raise NotImplementedError

    def all(self) -> list:
        raise NotImplementedError

    def count(self) -> int:
        raise NotImplementedError

    def clear(self) -> None:
        raise NotImplementedError
