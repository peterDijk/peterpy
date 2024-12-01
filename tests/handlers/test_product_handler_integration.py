import json
from unittest.mock import ANY, AsyncMock, Mock, patch

import pytest

from peterpy.entities import Product
from peterpy.services.product_service import ProductService
from tests.handlers import BaseHandlerTestCase
from tests.helpers import create_uuid_from_string


class TestProductHandlers(BaseHandlerTestCase):
    @patch(
        "peterpy.middlewares.ProductService",
        return_value=Mock(spec=ProductService),
    )
    @pytest.mark.asyncio
    async def test_add_product_integration(self, service_class_mock):
        """
        Test add product integration including the client,
        but mocking the service that is injected into the request
        in the middleware.
        ."""
        service = service_class_mock()
        product_added_request_integration = Product(
            product_id=create_uuid_from_string("product_added_request-1"),
            name="product_added_request",
            price=20.0,
            date_added="2021-01-01T00:00:00",
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
                "product_id": str(create_uuid_from_string("product_added_request-1")),
                "name": product_added_request_integration.name,
                "price": product_added_request_integration.price,
                "date_added": "2021-01-01T00:00:00",
            }
        }

    @pytest.mark.asyncio
    async def test_add_one_product_integration(self):
        """
        Test add one product integration including the client,
        without mocking the service that is injected into the request
        in the middleware.
        ."""
        product_added_request_integration = Product(
            product_id=create_uuid_from_string("product_added_request-1"),
            name="product_added_request",
            price=20.0,
        )

        response = await self.client.request(
            "POST",
            "/product",
            json={
                "name": product_added_request_integration.name,
                "price": product_added_request_integration.price,
            },
        )

        assert response.status == 201
        response_body = await response.text()
        assert json.loads(response_body) == {
            "product": {
                "product_id": ANY,
                "name": product_added_request_integration.name,
                "price": product_added_request_integration.price,
                "date_added": ANY,
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

    @pytest.mark.skip
    @pytest.mark.asyncio
    async def test_list_products_integration(self):
        """
        Test list products integration including the client
        """
        response = await self.client.request("GET", "/product/list")

        assert response.status == 200
        response_body = await response.text()
        assert json.loads(response_body) == {
            "products": [
                {
                    "product_id": str(create_uuid_from_string("p10")),
                    "name": "product_10",
                    "price": 10.0,
                    "date_added": ANY,
                },
                {
                    "product_id": str(create_uuid_from_string("p20")),
                    "name": "product_20",
                    "price": 10.0,
                    "date_added": ANY,
                },
            ]
        }
