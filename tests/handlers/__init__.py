from unittest.mock import Mock

from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase

from peterpy.app import setup_routes
from peterpy.database.connection import DatabaseConnection
from peterpy.database.models.base import Base
from peterpy.middlewares import db_session_wrapper_factory


class BaseHandlerTestCase(AioHTTPTestCase):

    async def get_application(self):
        connection = DatabaseConnection("sqlite:///:memory:")
        Base.metadata.create_all(connection.engine())
        app = web.Application(middlewares=[db_session_wrapper_factory(connection)])
        setup_routes(app)

        # need to find a way to drop the tables after the tests
        return app
