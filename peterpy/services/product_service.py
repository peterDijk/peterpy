import logging
from typing import Dict

from peterpy.entities import Product
from peterpy.interfaces import IRepository


class ProductService:
    def __init__(self, repository: IRepository[Product]):
        self._repository = repository

    def add(self, name: str, price: float) -> Product:
        if len(self._repository.find({"name": name})) > 0:
            raise ValueError(f"Product with name {name} already exists")

        product = Product(name=name, price=price)
        logging.debug("Adding product %s", product)
        logging.debug(product.__dict__)

        return self._repository.add(product)

    def update(self, product_id, name, price):
        product = self._repository.get(product_id)
        if not product:
            raise KeyError(f"Product with product_id {product_id} not found")

        if name:
            product.update_name(name)

        if price:
            product.update_price(price)

        return self._repository.update(product)

    def remove(self, product_id):
        product = self._repository.get(product_id)
        if not product:
            raise KeyError(f"Product with product_id {product_id} not found")

        self._repository.remove(product)

    def get(self, product_id):
        product = self._repository.get(product_id)
        return product

    def find(self, query: Dict[str, str]):
        return self._repository.find(query)

    def find_one(self, product_id):
        return self._repository.find_one(product_id)

    def all(self):
        return self._repository.all()

    def count(self):
        return self._repository.count()
