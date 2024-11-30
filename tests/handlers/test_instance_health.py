from textwrap import dedent
from unittest.mock import MagicMock, Mock

from aiohttp.web import Request

from peterpy.handlers.health_handler import instance_health
from peterpy.helpers import PeterRequest
from peterpy.services.product_service import ProductService
from tests.handlers import BaseHandlerTestCase


class TestHealthcheck(BaseHandlerTestCase):
    """Test healthcheck endpoint."""

    async def test_integration_health_check(self):
        response = await self.client.request("GET", "/health")
        assert response.status == 200

        response_text = await response.text()
        expected_response_text = dedent(
            """
            # HELP health_instance Instance health
            # TYPE health_instance gauge
            # PETERPY_VERSION: 0.1.0
            # health_instance{version="0.1.0"} 1.0
            """
        )

        assert response_text == expected_response_text

    async def test_unit_health_check(self):

        request = MagicMock(spec=PeterRequest)
        request.product_service = MagicMock(spec=ProductService)
        request.product_service.all.return_value = []
        response = await instance_health(request)

        assert response.status == 200

        # different because now we are testing the method and its output. above test we use the client which is an integration test which uses async getting the text
        response_text = response.text
        expected_response_text = dedent(
            """
            # HELP health_instance Instance health
            # TYPE health_instance gauge
            # PETERPY_VERSION: 0.1.0
            # health_instance{version="0.1.0"} 1.0
            """
        )

        assert response_text == expected_response_text
