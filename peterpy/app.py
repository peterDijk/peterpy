import asyncio
import logging
import logging.config
import sys
from os import EX_OK
from signal import SIGINT, SIGTERM

import uvloop
from aiohttp import web

from peterpy import __version__
from peterpy.config import config, environment
from peterpy.database.connection import DatabaseConnection, DatabaseSession
from peterpy.database.models import Product
from peterpy.handlers import health, products


@web.middleware
async def db_session_wrapper(request, handler):
    logging.debug("db_session_wrapper called")
    db_connection = DatabaseConnection()
    engine = db_connection.engine()

    try:
        with DatabaseSession(engine) as session:
            request["session"] = session
            response = await handler(request)
            session.commit()
            logging.debug("db_session_wrapper finished")
            return response
    except Exception as e:
        logging.exception("Exception happened in middleware 1")
        session.rollback()
        return web.json_response(status=500, text=str(e))


async def startup():
    logging.info("Starting app - version %s - environment %s", __version__, environment)

    # Web app
    http_app = web.Application(middlewares=[db_session_wrapper])
    setup_routes(http_app)
    http_host = config["APP_HOST"]
    http_port = config["APP_PORT"]

    http_runner = web.AppRunner(http_app)
    await http_runner.setup()

    site = web.TCPSite(http_runner, host=http_host, port=http_port)
    await site.start()

    logging.info("Starting web server, listening on %s:%s", http_host, http_port)

    # Setup signal handlers for graceful shutdown
    for signal in (SIGTERM, SIGINT):
        asyncio.get_running_loop().add_signal_handler(
            signal, lambda: asyncio.create_task(shutdown(http_runner))
        )

    # Sleep forever (until shutdowns called) to handle HTTP
    while True:
        await asyncio.sleep(3600)


def setup_routes(app: web.Application):
    app.router.add_get("/health", health.instance_health)
    app.router.add_get("/", products.get_dashboard)
    app.router.add_get("/product/list", products.list_products)
    app.router.add_get("/product/{id}", products.get_product)
    app.router.add_post("/product", products.add_product)


async def shutdown(http_runner: web.AppRunner):
    try:
        logging.info("[SHUTDOWN] Shutting down due to signal")

        logging.info("[SHUTDOWN] Shutting down HTTP stack")
        # close DB Connection
        await http_runner.shutdown()
        await http_runner.cleanup()
        sys.exit(EX_OK)
    except Exception:  # pylint: disable=broad-exception-caught
        # never happens
        logging.exception("Exception happened in signal handler!")


def main():
    logging.config.dictConfig(config)
    logging.info("Booting ....")

    db_connection = DatabaseConnection()
    engine = db_connection.engine()
    Product.metadata.create_all(engine)
    # move above to FLyway migrations in follow up PR

    # Open Database connection

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    asyncio.run(startup())


if __name__ == "__main__":
    main()
