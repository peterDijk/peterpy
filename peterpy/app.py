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
from peterpy.handlers import health, products

from peterpy.database.models import Product


async def startup(db_connection: DatabaseConnection):
    logging.info("Starting app - version %s - environment %s", __version__, environment)

    # Web app
    http_app = web.Application()
    setup_routes(http_app)
    http_host = config["app"]["host"]
    http_port = config["app"]["port"]

    http_runner = web.AppRunner(http_app)
    await http_runner.setup()

    # what is tcpsite for ?
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
    app.router.add_get("/health", health.instance_health)
    app.router.add_get("/", products.get_dashboard)
    app.router.add_get("/product/list", products.list_products)
    app.router.add_get("/product/{id}", products.get_product)
    app.router.add_post("/product", products.add_product)


async def shutdown(http_runner: web.AppRunner, db_connection: DatabaseConnection):
    try:
        logging.info("[SHUTDOWN] Shutting down due to signal")

        logging.info("[SHUTDOWN] Shutting down HTTP stack")
        db_connection.__exit__()
        await http_runner.shutdown()
        await http_runner.cleanup()
        sys.exit(EX_OK)
    except Exception:  # pylint: disable=broad-exception-caught
        # never happens
        logging.exception("Exception happened in signal handler!")


def main():
    logging.config.dictConfig(config)
    logging.info("Booting ....")

    # where to best do this migration ? separate script ?
    db_connection = DatabaseConnection()
    engine = db_connection.__enter__()
    Product.metadata.create_all(engine)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    asyncio.run(startup(db_connection))


if __name__ == "__main__":
    main()
