from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase

from peterpy.app import setup_routes
from peterpy.handlers.health_handler import instance_health


class BaseHandlerTestCase(AioHTTPTestCase):
    async def get_application(self):
        app = web.Application()
        setup_routes(app)

        return app
