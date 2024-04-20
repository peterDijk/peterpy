import asyncio
import logging
import logging.config
import uvloop
from signal import SIGINT, SIGTERM
from os import EX_OK
import sys
from aiohttp import web

from peterpy.config import config, environment
from peterpy import __version__

from peterpy.handlers import health

async def startup():
   logging.info(f"Starting app - version {__version__} - environment {environment}")

   #Web app
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
         signal,
         lambda: asyncio.create_task(
             shutdown(http_runner)
         )
      )
     
     
   # Sleep forever (until shutdowns called) to handle HTTP
   while True:
     await asyncio.sleep(3600)


def setup_routes(app: web.Application):
   app.router.add_get("/health", health.instance_health)
   app.router.add_get("/", health.instance_health)
   
async def shutdown(http_runner: web.AppRunner):
   try:
     logging.info("[SHUTDOWN] Shutting down due to signal")

     logging.info("[SHUTDOWN] Shutting down HTTP stack")
     await http_runner.shutdown()
     await http_runner.cleanup()
     sys.exit(EX_OK)
   except Exception:  # pylint: disable=broad-exception-caught
      # never happens
      logging.exception("Exception happened in signal handler!")

def main():
   logging.config.dictConfig(config)
   logging.info("Booting ... info")
   logging.debug("Booting ... debug")
   logging.info("Booting ... info")
   logging.critical("Booting ... critical")
   logging.error("Booting ... error")
   logging.warning("Booting ... warning")
   logging.exception("Booting ... exception")
   logging.warning("Booting ... warning")
   
   asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
   asyncio.run(startup())

if __name__ == "__main__":
   main()