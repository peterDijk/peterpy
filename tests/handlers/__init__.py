from unittest.mock import Mock
from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase

from peterpy.app import setup_routes
from peterpy.database.connection import DatabaseConnection
from peterpy.middlewares import db_session_wrapper_factory


class BaseHandlerTestCase(AioHTTPTestCase):

    async def get_application(self):
        db_connection = Mock(spec=DatabaseConnection)
        app = web.Application(middlewares=[db_session_wrapper_factory(db_connection)])
        setup_routes(app)

        return app
