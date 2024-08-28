import json
from unittest.mock import MagicMock

from peterpy.entities import Product
from peterpy.handlers.product_handler import list_products
from peterpy.interfaces.request import PeterRequest
from tests.handlers import BaseHandlerTestCase
from tests.helpers import create_uuid_from_string

product_1 = Product(
    product_id=create_uuid_from_string("product_1"), name="product_1", price=10.0
)
product_2 = Product(
    product_id=create_uuid_from_string("product_2"), name="product_2", price=20.0
)


def products_generator():
    yield product_1
    yield product_2


class TestHealthcheck(BaseHandlerTestCase):
    async def test_list_products(self):
        request = MagicMock(spec=PeterRequest)
        request.product_service.all.return_value = products_generator()
        response = await list_products(request)
        assert response.status == 200
        response_json = json.loads(response.text)
        assert response_json["products"][0]["name"] == "product_1"
        assert response_json["products"][1]["name"] == "product_2"
