import logging
from typing import Dict

from peterpy.entities import Product
from peterpy.interfaces import IRepository


class ProductService:
    def __init__(self, repository: IRepository[Product]):
        self._repository = repository

    def add(self, name: str, price: float) -> Product:
        if self._repository.find({"name": name}):
            raise KeyError(f"Product with name {name} already exists")

        product = Product(name, price)
        logging.debug(f"Adding product {product}")
        self._repository.add(product)

        return product

    def update(self, id, name, price):
        product = self._repository.get(id)
        if not product:
            raise KeyError(f"Product with id {id} not found")

        if name:
            product.update_name(name)

        if price:
            product.update_price(price)

        self._repository.update(product)

    def remove(self, id):
        product = self._repository.get(id)
        if not product:
            raise KeyError(f"Product with id {id} not found")

        self._repository.remove(product)

    def get(self, id):
        return self._repository.get(id)

    def find(self, query: Dict[str, str]):
        return self._repository.find(query)

    def find_one(self, id):
        return self._repository.find_one(id)

    def all(self):
        return self._repository.all()

    def count(self):
        return self._repository.count()
