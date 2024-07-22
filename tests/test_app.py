from aiohttp.web_request import Request
from textwrap import dedent

import pytest
from asynctest import Mock  # type: ignore

from peterpy.handlers import health_handler


@pytest.mark.asyncio
async def test_health_check():
    """Test health check endpoint"""
    response = await health_handler(Mock(spec=Request))
    assert response.status == 200
    response_text = """
        # HELP health_instance Instance health
        # TYPE health_instance gauge
        # PETERPY_VERSION: 0.1.0
        health_instance{version="0.1.0"} 1.0 
        """
    assert response.text == dedent(response_text)
