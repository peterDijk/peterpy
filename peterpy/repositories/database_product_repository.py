import logging
from typing import Dict, List
from uuid import UUID

from peterpy.entities import Product as ProductEntity
from peterpy.interfaces import IRepository

from peterpy.database.connection import DatabaseSession, engine

from sqlalchemy import select
from sqlalchemy.orm import Session

from peterpy.database.data_mapper import (
    product_model_to_entity,
    product_entity_to_model,
)

from peterpy.database.models.product import Product as ProductModel

db_session = DatabaseSession()


class DatabaseProductRepository(IRepository[ProductEntity]):
    def get(self, id: UUID) -> ProductEntity:
        session = db_session.__enter__()
        sql_statement = select(ProductModel).filter(ProductModel.id == id.__str__())
        product = session.execute(sql_statement).scalar_one_or_none()
        if product:
            return product_model_to_entity(product)

        raise KeyError(f"Product with id {id} not found")

    def add(self, obj: ProductEntity) -> None:
        instance = product_entity_to_model(obj)
        session = db_session.__enter__()
        session.add(instance)
        session.commit()

    def update(self, obj: ProductEntity) -> None:
        raise NotImplementedError

    def remove(self, obj: ProductEntity) -> None:
        raise NotImplementedError

    def find(self, query: Dict[str, str]) -> list:
        items: List[ProductEntity] = []

        for key, value in query.items():
            session = db_session.__enter__()
            sql_statement = select(ProductModel).filter(
                getattr(ProductModel, key) == value
            )
            results = [
                product_model_to_entity(product[0])
                for product in session.execute(sql_statement)
            ]
            items.extend(results)

        return items

    def find_one(self, id: UUID) -> ProductEntity:
        raise NotImplementedError

    def all(self) -> list:
        session = db_session.__enter__()
        stmt = select(ProductModel).order_by(ProductModel.id)
        return [
            product_model_to_entity(product[0]) for product in session.execute(stmt)
        ]

    def count(self) -> int:
        session = db_session.__enter__()
        stmt = select(ProductModel).order_by(ProductModel.id)
        return [
            product_model_to_entity(product[0]) for product in session.execute(stmt)
        ].__len__()

    def clear(self) -> None:
        raise NotImplementedError
