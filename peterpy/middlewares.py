import logging

from aiohttp import web
from aiohttp.web import Request

from peterpy.database import DatabaseConnection, DatabaseSession
from peterpy.helpers import json_response
from peterpy.interfaces import PeterRequest
from peterpy.repositories import DatabaseProductRepository
from peterpy.services import ProductService


def db_session_wrapper_factory(db_connection: DatabaseConnection):
    @web.middleware
    async def db_session_wrapper(request: Request, handler):
        logging.debug("db_session_wrapper called")

        print("db_connection", db_connection)
        engine = db_connection.engine()

        peter_request = PeterRequest(request)

        with DatabaseSession(engine) as session:
            print("session", session)
            try:
                repository = DatabaseProductRepository(session)
                product_service = ProductService(repository)
                peter_request.product_service = product_service

                print("peter_request", peter_request)

                response = await handler(peter_request)
                logging.debug("db_session_wrapper committing")
                session.commit()
                logging.debug("db_session_wrapper finished")
                return response
            except Exception as e:
                logging.error(
                    "Exception happened in db_session_wrapper - rolling back. Exception: %s",
                    e,
                )
                session.rollback()
                return json_response(
                    status=500,
                    content={"message": "Internal Server Error", "error": str(e)},
                )

    return db_session_wrapper
