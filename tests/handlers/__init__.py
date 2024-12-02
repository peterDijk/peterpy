from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase

from peterpy.app import setup_routes
from peterpy.database.connection import DatabaseConnection, DatabaseSession
from peterpy.database.models.base import Base
from peterpy.database.models.product import Product
from peterpy.middlewares import db_session_wrapper_factory
from tests.helpers import create_uuid_from_string


class BaseHandlerTestCase(AioHTTPTestCase):
    async def get_application(self):
        connection = DatabaseConnection("sqlite:///:memory:")
        self.connection = connection
        Base.metadata.create_all(connection.engine())

        app = web.Application(middlewares=[db_session_wrapper_factory(connection)])
        setup_routes(app)

        return app

    async def tearDownAsync(self):
        # Cleanup method to drop tables after tests
        print("Dropping tables")
        Base.metadata.drop_all(self.connection.engine())
        await super().tearDownAsync()
