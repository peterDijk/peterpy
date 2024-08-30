import json
import pytest
from unittest.mock import MagicMock

from peterpy.entities import Product
from peterpy.handlers.product_handler import list_products, add_product
from peterpy.interfaces.request import PeterRequest
from peterpy.services.product_service import ProductService
from tests.handlers import BaseHandlerTestCase
from tests.helpers import create_uuid_from_string

product_1 = Product(
    product_id=create_uuid_from_string("product_1"), name="product_1", price=10.0
)
product_2 = Product(
    product_id=create_uuid_from_string("product_2"), name="product_2", price=20.0
)
product_added_request = Product(
    product_id=create_uuid_from_string("product_added_request"),
    name="product_added_request",
    price=20.0,
)


def products_generator():
    yield product_1
    yield product_2


class TestProductHandlers(BaseHandlerTestCase):
    async def test_list_products(self):
        request = MagicMock(spec=PeterRequest)
        request.product_service = MagicMock(spec=ProductService)
        request.product_service.all.return_value = products_generator()
        response = await list_products(request)
        assert response.status == 200
        response_json = json.loads(response.text)
        assert response_json["products"][0]["name"] == "product_1"
        assert response_json["products"][1]["name"] == "product_2"

    # @pytest.mark.asyncio()
    @pytest.mark.skip()
    async def test_add_product(self):
        request = MagicMock(spec=PeterRequest)
        request.product_service = MagicMock(spec=ProductService)

        # request.body = {"name": "product_added_request", "price": 10.0}

        request.product_service.add.return_value = product_added_request
        response = await add_product(request)
        assert response.status == 201
        request.product_service.add.assert_awaited_once()
