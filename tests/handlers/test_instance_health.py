from textwrap import dedent

from tests.handlers import BaseHandlerTestCase

from peterpy.handlers import instance_health


class TestHealthcheck(BaseHandlerTestCase):
    """Test healthcheck endpoint."""

    async def test_health_check(self):
        response = await self.client.request("GET", "/health")

        assert response.status == 200
        response_text = "ok"

        assert response.text == response_text
