from typing import Dict
from peterpy.repositories import MemoryProductRepository
from peterpy.entities import Product


class ProductService:
    def __init__(self, repository: MemoryProductRepository):
        self._repository = repository

    def add(self, name: str, price: float):
        product = Product(name, price)
        self._repository.add(product)

    def update(self, id, name, price):
        product = self._repository.get(id)
        if not product:
            raise KeyError(f"Product with id {id} not found")

        if name:
            product.update_name(name)

        if price:
            product.update_price(price)

        self._repository.update(product)

    def get(self, id):
        return self._repository.get(id)

    def remove(self, id):
        product = self._repository.get(id)
        if not product:
            raise KeyError(f"Product with id {id} not found")

        self._repository.remove(product)

    def find(self, query: Dict[str, Product]):
        return self._repository.find(query)

    def find_one(self, id):
        return self._repository.find_one(id)

    def all(self):
        return self._repository.all()
