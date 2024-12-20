import logging
from typing import Dict, Generator, List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from peterpy.database.data_mapper import (
    product_entity_to_model,
    product_model_to_entity,
)
from peterpy.database.models.product import Product as ProductModel
from peterpy.entities import Product as ProductEntity
from peterpy.interfaces import IRepository


class DatabaseProductRepository(IRepository[ProductEntity]):
    def __init__(self, session: Session):
        self.session = session

    def flush(self):
        self.session.flush()

    def get(self, product_id: UUID) -> ProductEntity:
        sql_statement = select(ProductModel).filter(
            ProductModel.product_id == str(product_id)
        )
        product = self.session.execute(sql_statement).scalar_one_or_none()
        if product:
            return product_model_to_entity(product)

        raise KeyError(f"Product with product_id {product_id} not found")

    def add(self, obj: ProductEntity, flush=False) -> ProductEntity:
        try:
            instance = product_entity_to_model(obj)
            self.session.add(instance)

            if flush:
                self.flush()

            return obj
        except IntegrityError as e:
            logging.error("Failed to add product: %s", e)
            raise ValueError("Failed to add product: IntegrityError") from e

    # pylint: disable=unused-argument
    def update(self, obj: ProductEntity) -> ProductEntity:
        raise NotImplementedError

    # pylint: disable=unused-argument
    def remove(self, obj: ProductEntity) -> ProductEntity:
        raise NotImplementedError

    def find(self, query: Dict[str, str]) -> list:
        items: List[ProductEntity] = []

        for key, value in query.items():
            sql_statement = select(ProductModel).filter(
                getattr(ProductModel, key) == value
            )
            results = [
                product_model_to_entity(product[0])
                for product in self.session.execute(sql_statement)
            ]
            items.extend(results)

        return items

    # pylint: disable=unused-argument
    def find_one(self, obj_id: UUID) -> ProductEntity:
        raise NotImplementedError

    def all(self) -> Generator[ProductEntity, None, None]:
        stmt = select(ProductModel).order_by(ProductModel.date_added.desc())
        for product in self.session.execute(stmt):
            entity = product_model_to_entity(product[0])
            yield entity

    def count(self) -> int:
        products = self.all()
        return len(list(products))

    def clear(self) -> None:
        raise NotImplementedError
