import json
from unittest.mock import AsyncMock, Mock
from aiohttp.web import Request

import pytest

from peterpy.entities import Product
from peterpy.handlers.product_handler import add_product, list_products
from peterpy.services.product_service import ProductService
from tests.helpers import create_uuid_from_string


@pytest.fixture
def test_products():
    product_1 = Product(
        product_id=create_uuid_from_string("product_1"),
        name="product_1",
        price=10.0,
        date_added="2021-01-01T00:00:00",
    )
    product_2 = Product(
        product_id=create_uuid_from_string("product_2"),
        name="product_2",
        price=20.0,
        date_added="2021-01-01T00:00:00",
    )
    return [product_1, product_2]


@pytest.mark.asyncio
async def test_list_products(test_products):
    def products_generator():
        yield test_products[0]
        yield test_products[1]

    request = Mock(spec=Request)
    request.__getitem__ = Mock(spec=ProductService)
    request["product_service"].all.return_value = products_generator()
    response = await list_products(request)
    assert response.status == 200
    response_json = json.loads(response.text)
    assert response_json["products"][0]["name"] == "product_1"
    assert response_json["products"][1]["name"] == "product_2"


@pytest.mark.asyncio
async def test_add_product_unit(test_products):
    request = Mock(spec=Request)
    request.__getitem__ = Mock(spec=ProductService)
    request.json.return_value = {
        "name": "test_product_added_request",
        "price": 10.0,
    }

    request["product_service"].add = AsyncMock(return_value=test_products[0])

    response = await add_product(request)

    request["product_service"].add.assert_called_once_with(
        "test_product_added_request", 10.0
    )

    assert response.status == 201
    assert json.loads(response.body) == {
        "product": {
            "product_id": str(create_uuid_from_string("product_1")),
            "name": "product_1",
            "price": 10.0,
            "date_added": "2021-01-01T00:00:00",
        }
    }
