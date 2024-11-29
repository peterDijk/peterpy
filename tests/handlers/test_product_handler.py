import json
import pytest
from unittest.mock import Mock, AsyncMock, AsyncMockMixin, patch

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
product_added_id = create_uuid_from_string("product_added_request")
product_added_request = Product(
    product_id=product_added_id,
    name="product_added_request",
    price=10.0,
)


def products_generator():
    yield product_1
    yield product_2


class TestProductHandlers(BaseHandlerTestCase):
    @pytest.mark.skip
    @pytest.mark.asyncio
    async def test_list_products(self):
        request = Mock(spec=PeterRequest)
        request.product_service = Mock(spec=ProductService)
        request.product_service.all.return_value = products_generator()
        response = await list_products(request)
        assert response.status == 200
        response_json = json.loads(response.text)
        assert response_json["products"][0]["name"] == "product_1"
        assert response_json["products"][1]["name"] == "product_2"

    @pytest.mark.skip
    @pytest.mark.asyncio
    async def test_add_product(self):
        """
        I would like to test the handler using the aiohttp test client,
        but because of the implementation of adding the service to the request
        in the middleware wrapper, that would be complicated.
        I would have to construct the middleware,
        """
        request = Mock(spec=PeterRequest)
        request.product_service = Mock(spec=ProductService)
        request.json.return_value = {
            "name": "test_product_added_request",
            "price": 10.0,
        }

        request.product_service.add = AsyncMock(return_value=product_added_request)

        response = await add_product(request)

        request.product_service.add.assert_called_once_with(
            "test_product_added_request", 10.0
        )

        assert response.status == 201
        assert json.loads(response.body) == {
            "product": {
                "product_id": str(product_added_id),
                "name": "product_added_request",
                "price": 10.0,
            }
        }

    # @pytest.mark.skip
    @patch(
        "peterpy.middlewares.ProductService",
        return_value=Mock(spec=ProductService),
    )  # what is lambda ?
    @pytest.mark.asyncio
    async def test_add_product_by_client(self, service_mock):
        service = service_mock()
        service.add = AsyncMock(return_value=product_added_request)

        response = await self.client.request(
            "POST",
            "/product",
            json={"name": "product_added_request", "price": 20.0},
        )

        assert response.status == 201
