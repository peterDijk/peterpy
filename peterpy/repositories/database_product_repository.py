import logging
from typing import Dict, List
from uuid import UUID

from peterpy.entities import Product as ProductEntity
from peterpy.interfaces import IRepository

from peterpy.database.connection import DatabaseSession

from sqlalchemy import select

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
            db_session.__exit__()
            return product_model_to_entity(product)

        raise KeyError(f"Product with id {id} not found")

    def add(self, product_entity: ProductEntity) -> ProductEntity:
        instance = product_entity_to_model(product_entity)
        session = db_session.__enter__()
        session.add(instance)
        session.commit()
        db_session.__exit__()

        return product_entity

    def update(self, product_entity: ProductEntity) -> ProductEntity:
        raise NotImplementedError

    def remove(self, product_entity: ProductEntity) -> ProductEntity:
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

        db_session.__exit__()

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
