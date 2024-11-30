import json
from unittest.mock import AsyncMock, AsyncMockMixin, Mock, patch

import pytest

from peterpy.entities import Product
from peterpy.handlers.product_handler import add_product, list_products
from peterpy.helpers import PeterRequest
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

    @pytest.mark.asyncio
    async def test_add_product_unit(self):
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

    @patch(
        "peterpy.middlewares.ProductService",
        return_value=Mock(spec=ProductService),
    )  # what is lambda ?
    @pytest.mark.asyncio
    async def test_add_product_integration(self, service_class_mock):
        """
        Test add product integration including the client,
        but mocking the service that is injected into the request
        in the middleware.
        ."""
        service = service_class_mock()
        product_added_request_integration = Product(
            product_id=product_added_id,
            name="product_added_request",
            price=20.0,
        )

        service.add = AsyncMock(return_value=product_added_request_integration)

        response = await self.client.request(
            "POST",
            "/product",
            json={
                "name": product_added_request_integration.name,
                "price": product_added_request_integration.price,
            },
        )

        service.add.assert_called_once_with(
            product_added_request_integration.name,
            product_added_request_integration.price,
        )

        assert response.status == 201
        response_body = await response.text()
        assert json.loads(response_body) == {
            "product": {
                "product_id": str(product_added_id),
                "name": product_added_request_integration.name,
                "price": product_added_request_integration.price,
            }
        }

    @pytest.mark.asyncio
    async def test_add_products_and_dashboard_integration(self):
        """
        Test add products and dashboard full integration, without any mocks
        from making the request to the client, where the service
        is setup correctly using the repository which is setup
        in the middleware using the connection that is setup
        using Sqlite setup in the BaseHandlerTestCase.
        """
        product_added_request_integration = Product(
            product_id=create_uuid_from_string("product_added_request-1"),
            name="product_added_request",
            price=20.0,
        )
        product_added_request_integration2 = Product(
            product_id=create_uuid_from_string("product_added_request-2"),
            name="product_added_request 2",
            price=50.0,
        )

        response = await self.client.request(
            "POST",
            "/products",
            json={
                "products": [
                    {
                        "name": product_added_request_integration.name,
                        "price": product_added_request_integration.price,
                    },
                    {
                        "name": product_added_request_integration2.name,
                        "price": product_added_request_integration2.price,
                    },
                ]
            },
        )

        assert response.status == 201

        response_dash = await self.client.request(
            "GET",
            "/",
        )

        assert response_dash.status == 200
        response_body = await response_dash.text()
        assert json.loads(response_body) == {
            "dashboard": {
                "products_count": 2,
                "products_total_value": 70.0,
            }
        }
