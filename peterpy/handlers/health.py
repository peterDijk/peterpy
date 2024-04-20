from textwrap import dedent
from uuid import UUID

import logging

from aiohttp.web import Request, Response

from peterpy import __version__, routes

# pylint: disable=unused-argument
@routes.get("/health")
async def instance_health(request: Request) -> Response:
    logging.info(f"Health check requested from {request.remote}")
    
    output = dedent(
        """
        # HELP health_instance Instance health
        # TYPE health_instance gauge
        # PETERPY_VERSION: {version}
        health_instance{{version="{version}"}} 1.0        
        
        """
    ).format(version=__version__)
    return Response(status=200, body=output)