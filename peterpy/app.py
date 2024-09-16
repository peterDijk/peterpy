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
from peterpy.database.connection import DatabaseConnection
from peterpy.database.models.product import Product
from peterpy.handlers import health_handler, product_handler
from peterpy.middlewares import db_session_wrapper_factory


async def startup(db_connection: DatabaseConnection):
    logging.info("Starting app - version %s - environment %s", __version__, environment)

    # Web app
    http_app = web.Application(middlewares=[db_session_wrapper_factory(db_connection)])
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
            signal, lambda: asyncio.create_task(shutdown(http_runner, db_connection))
        )

    # Sleep forever (until shutdowns called) to handle HTTP
    while True:
        await asyncio.sleep(3600)


def setup_routes(app: web.Application):
    app.router.add_get("/health", health_handler.instance_health)
    app.router.add_get("/", product_handler.get_dashboard)
    app.router.add_get("/product/list", product_handler.list_products)
    app.router.add_get("/product/{id}", product_handler.get_product)
    app.router.add_post("/product", product_handler.add_product)
    app.router.add_post("/products", product_handler.add_products)


async def shutdown(http_runner: web.AppRunner, db_connection: DatabaseConnection):
    try:
        logging.info("[SHUTDOWN] Shutting down due to signal")

        logging.info("[SHUTDOWN] Shutting down HTTP stack")
        # close DB Connection
        db_connection.close()
        await http_runner.shutdown()
        await http_runner.cleanup()
        sys.exit(EX_OK)
    except Exception:  # pylint: disable=broad-exception-caught
        # never happens
        logging.exception("Exception happened in signal handler!")


def main():
    logging.config.dictConfig(config)
    logging.info("Booting ....")

    try:
        # Open Database connection
        db_connection = DatabaseConnection()

        engine = db_connection.engine()
        Product.metadata.create_all(engine)
        # move above to FLyway migrations in follow up PR

        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        asyncio.run(startup(db_connection))
    except Exception as e:
        print(f"Error connecting to database: {e}")


if __name__ == "__main__":
    main()
