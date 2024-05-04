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
from peterpy.database.models import Product
from peterpy.handlers import health, products


async def startup():
    logging.info("Starting app - version %s - environment %s", __version__, environment)

    # Web app
    http_app = web.Application()
    setup_routes(http_app)
    http_host = config["APP_HOST"]
    http_port = config["APP_PORT"]

    http_runner = web.AppRunner(http_app)
    await http_runner.setup()

    # what is tcpsite for ?
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
        # close connection ?
        # it was already closed in the __exit__ method of DatabaseConnection using the with statement
        # in main() function
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
    with DatabaseConnection() as engine:
        Product.metadata.create_all(engine)
    # connection is closed now because of __exit__ method
    # how should i organise this so that connections remains open
    # for the lifetime of the app, and I close the connection in the shutdown function?
    # Should the connection remain open for the lifetime of the app, and open/close Sessions per request ? or should I open/close the connection per request ?

    """
    In general, it's a good practice to minimize the number of open connections and to close connections as soon as they are no longer needed. This helps to conserve resources and prevent issues such as connection leaks, where connections remain open indefinitely and consume resources.
    thanks copilot
    """

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    asyncio.run(startup())


if __name__ == "__main__":
    main()
