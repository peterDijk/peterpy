from datetime import datetime, timedelta
import json
import os
from unittest.mock import ANY, AsyncMock, Mock, patch

import pytest

from peterpy.database.connection import DatabaseSession
from peterpy.entities import Product
from peterpy.database.models.product import Product as ProductModel
from peterpy.services.product_service import ProductService
from tests.handlers import BaseHandlerTestCase
from tests.helpers import create_uuid_from_string


def load_json_file(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


mock_products_file_path = os.path.join(
    os.path.dirname(__file__), "..", "mock-products.json"
)
mock_data = load_json_file(mock_products_file_path)


class TestProductHandlers(BaseHandlerTestCase):
    def seed(self):
        mock_products = []
        for index, product in enumerate(mock_data):
            date_added = datetime.now() - timedelta(days=1) + timedelta(minutes=index)
            product_model = ProductModel(
                product_id=str(create_uuid_from_string(product["name"])),
                name=product["name"],
                price=product["price"],
                date_added=date_added,
            )
            mock_products.append(product_model)

        with DatabaseSession(self.connection.engine()) as session:
            for product in mock_products:
                session.add(product)
            session.commit()

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
            product_id=create_uuid_from_string("Apple"),
            name="Apple",
            price=10.0,
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
    async def test_dashboard_integration(self):
        """
        Test add products and dashboard full integration, without any mocks
        from making the request to the client, where the service
        is setup correctly using the repository which is setup
        in the middleware using the connection that is setup
        using Sqlite setup in the BaseHandlerTestCase.
        """

        self.seed()

        response_dash = await self.client.request(
            "GET",
            "/",
        )

        assert response_dash.status == 200
        response_body = await response_dash.text()

        assert json.loads(response_body) == {
            "dashboard": {
                "products_count": 11,
                "products_total_value": 5190,
            }
        }

    @pytest.mark.asyncio
    async def test_list_products_integration(self):
        """
        Test list products integration including the client
        """
        self.seed()

        response = await self.client.request("GET", "/product/list?page=1&limit=5")
        assert response.status == 200
        response_body = await response.text()
        assert len(json.loads(response_body)["products"]) == 5
        assert (json.loads(response_body)["products"][0]) == {
            "product_id": str(create_uuid_from_string("Another Tamarillo")),
            "name": "Another Tamarillo",
            "price": 500.0,
            "date_added": ANY,
        }

        response2 = await self.client.request("GET", "/product/list?page=2&limit=5")
        assert response2.status == 200
        response_body2 = await response2.text()
        assert len(json.loads(response_body2)["products"]) == 5
        assert (json.loads(response_body2)["products"][0]) == {
            "product_id": str(create_uuid_from_string("Oregon Grape")),
            "name": "Oregon Grape",
            "price": 470.0,
            "date_added": ANY,
        }

        response3 = await self.client.request("GET", "/product/list?page=3&limit=5")
        assert response3.status == 200
        response_body3 = await response3.text()
        assert len(json.loads(response_body3)["products"]) == 1
        assert (json.loads(response_body3)["products"][0]) == {
            "product_id": str(create_uuid_from_string("Jostaberry")),
            "name": "Jostaberry",
            "price": 445.0,
            "date_added": ANY,
        }

    @pytest.mark.asyncio
    async def test_get_one_product_integration(self):
        """Test get one product endpoint"""
        self.seed()
        response = await self.client.request(
            "GET", f"/product/{str(create_uuid_from_string("Tamarillo"))}"
        )

        assert response.status == 200
        response_body = await response.text()
        assert json.loads(response_body) == {
            "product": {
                "product_id": str(create_uuid_from_string("Tamarillo")),
                "name": "Tamarillo",
                "price": 495.0,
                "date_added": ANY,
            }
        }
