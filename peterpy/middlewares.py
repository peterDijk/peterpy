from aiohttp import web
import logging

from peterpy.database.connection import DatabaseConnection, DatabaseSession
from peterpy.repositories.database_product_repository import DatabaseProductRepository
from peterpy.services.product_service import ProductService


def db_session_wrapper_factory(db_connection: DatabaseConnection):
    @web.middleware
    async def db_session_wrapper(request, handler):
        logging.debug("db_session_wrapper called")
        engine = db_connection.engine()

        try:
            with DatabaseSession(engine) as session:
                repository = DatabaseProductRepository(session)
                product_service = ProductService(repository)
                request["product_service"] = product_service

                response = await handler(request)
                logging.debug("db_session_wrapper committing")
                session.commit()
                logging.debug("db_session_wrapper finished")
                return response
        except Exception as e:
            logging.exception(
                "Exception happened in db_session_wrapper 1: %s - rolling back", e
            )
            session.rollback()
            return web.json_response(status=500, text=str(e))

    return db_session_wrapper
