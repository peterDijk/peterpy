from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase

from peterpy import routes
from peterpy.handlers import instance_health


class BaseHandlerTestCase(AioHTTPTestCase):
    async def get_application(self):
        app = web.Application()
        app.add_routes(routes)

        return app
