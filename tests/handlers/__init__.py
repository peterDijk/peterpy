from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase

from peterpy import routes
from peterpy.handlers.health_handler import instance_health


class BaseHandlerTestCase(AioHTTPTestCase):
    async def get_application(self):
        app = web.Application()
        # app.add_routes(routes)
        # ook routes in app apart toevoegen
        app.router.add_get("/health", instance_health)

        return app
