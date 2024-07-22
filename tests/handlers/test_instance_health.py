from textwrap import dedent

from tests.handlers import BaseHandlerTestCase

from peterpy.handlers import instance_health


class TestHealthcheck(BaseHandlerTestCase):
    """Test healthcheck endpoint."""

    async def test_health_check(self):
        response = await self.client.request("GET", "/health")

        assert response.status == 200
        # response_text = """
        #     # HELP health_instance Instance health
        #     # TYPE health_instance gauge
        #     # PETERPY_VERSION: 0.1.0
        #     health_instance{version="0.1.0"} 1.0
        #     """

        # assert response.text == dedent(response_text)
