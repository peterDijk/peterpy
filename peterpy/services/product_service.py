import logging
from typing import Dict

from peterpy.entities import Product
from peterpy.interfaces import IRepository


class ProductService:
    def __init__(self, repository: IRepository[Product]):
        self.repository = repository

    async def add(self, name: str, price: float):
        product = Product(name=name, price=price)
        logging.debug("Adding product %s", product)

        stored_product = self.repository.add(product, flush=True)

        return stored_product

    def update(self, product_id, name, price):
        product = self.repository.get(product_id)
        if not product:
            raise KeyError(f"Product with product_id {product_id} not found")

        if name:
            product.update_name(name)

        if price:
            product.update_price(price)

        return self.repository.update(product)

    def remove(self, product_id):
        product = self.repository.get(product_id)
        if not product:
            raise KeyError(f"Product with product_id {product_id} not found")

        self.repository.remove(product)

    def get(self, product_id):
        logging.info("Getting product with product_id %s", product_id)
        product = self.repository.get(product_id)
        return product

    def find(self, query: Dict[str, str]):
        return self.repository.find(query)

    def find_one(self, product_id):
        return self.repository.find_one(product_id)

    def all(self):
        generator_products = self.repository.all()
        return generator_products

    def count(self):
        return self.repository.count()
