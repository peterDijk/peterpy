from uuid import UUID
import uuid


class Product:
    id: UUID
    name: str
    price: float

    def __init__(self, name: str, price: float):
        self.id = uuid.uuid4()
        self.name = name
        self.price = price

    def update_name(self, name: str):
        self.name = name

    def update_price(self, price: float):
        self.price = price

    def __str__(self):
        return f"{self.name} - ${self.price}"
