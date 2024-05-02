from typing import Dict, List
from uuid import UUID

from sqlalchemy import select

from peterpy.database.connection import DatabaseSession
from peterpy.database.data_mapper import (
    product_entity_to_model,
    product_model_to_entity,
)
from peterpy.database.models.product import Product as ProductModel
from peterpy.entities import Product as ProductEntity
from peterpy.interfaces import IRepository


class DatabaseProductRepository(IRepository[ProductEntity]):
    def get(self, product_id: UUID) -> ProductEntity:
        with DatabaseSession() as session:
            sql_statement = select(ProductModel).filter(
                ProductModel.product_id == str(product_id)
            )
            product = session.execute(sql_statement).scalar_one_or_none()
            if product:
                return product_model_to_entity(product)

        raise KeyError(f"Product with product_id {product_id} not found")

    def add(self, obj: ProductEntity) -> ProductEntity:
        instance = product_entity_to_model(obj)
        with DatabaseSession() as session:
            session.add(instance)
            session.commit()

        return obj

    # pylint: disable=unused-argument
    def update(self, obj: ProductEntity) -> ProductEntity:
        raise NotImplementedError

    # pylint: disable=unused-argument
    def remove(self, obj: ProductEntity) -> ProductEntity:
        raise NotImplementedError

    def find(self, query: Dict[str, str]) -> list:
        items: List[ProductEntity] = []

        for key, value in query.items():
            with DatabaseSession() as session:
                sql_statement = select(ProductModel).filter(
                    getattr(ProductModel, key) == value
                )
                results = [
                    product_model_to_entity(product[0])
                    for product in session.execute(sql_statement)
                ]
                items.extend(results)

        return items

    # pylint: disable=unused-argument
    def find_one(self, obj_id: UUID) -> ProductEntity:
        raise NotImplementedError

    def all(self) -> list:
        with DatabaseSession() as session:
            stmt = select(ProductModel).order_by(ProductModel.date_added)
            return [
                product_model_to_entity(product[0]) for product in session.execute(stmt)
            ]

    def count(self) -> int:
        with DatabaseSession() as session:
            stmt = select(ProductModel).order_by(ProductModel.date_added)
            return len(
                [
                    product_model_to_entity(product[0])
                    for product in session.execute(stmt)
                ]
            )

    def clear(self) -> None:
        raise NotImplementedError
