from unittest.mock import MagicMock, Mock, patch
from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase

from sqlalchemy.orm import Session

from peterpy.app import setup_routes
from peterpy.database.connection import DatabaseConnection, DatabaseSession
from peterpy.middlewares import db_session_wrapper_factory


class BaseHandlerTestCase(AioHTTPTestCase):

    async def get_application(self):
        app = web.Application()
        setup_routes(app)

        return app
