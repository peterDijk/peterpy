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

logger = logging.getLogger(environment)

async def startup():
   logger.info(f"Starting app - version {__version__} - environment {environment}")

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
   
   logger.info("Starting web server, listening on %s:%s", http_host, http_port)
   
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
     
def health_check(request):
   return web.Response(text="OK")

def setup_routes(app: web.Application):
   app.router.add_get("/health", health_check)
   app.router.add_get("/", health_check)
   
async def shutdown(http_runner: web.AppRunner):
   try:
     logger.info("[SHUTDOWN] Shutting down due to signal")

     logger.info("[SHUTDOWN] Shutting down HTTP stack")
     await http_runner.shutdown()
     await http_runner.cleanup()
   #   sys.exit(EX_OK)
   except Exception:  # pylint: disable=broad-exception-caught
      # never happens
      logger.exception("Exception happened in signal handler!")

def main():
   logging.config.dictConfig(config)
   logging.info("Starting up :)")
   asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
   asyncio.run(startup())

if __name__ == "__main__":
   main()