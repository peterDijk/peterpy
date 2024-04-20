import logging
import json

from aiohttp.web import Request, Response, json_response

from peterpy import routes
from peterpy.repositories import MemoryProductRepository
from peterpy.services import ProductService


@routes.get("/list")
async def list_products(request: Request) -> Response:
    logging.info("List products requested from %s", request.remote)

    product_repository = MemoryProductRepository()
    product_service = ProductService(product_repository)
    products = product_service.all()
    products_count = product_service.count()

    product_json = json.dumps({"products": products, "count": products_count})

    return json_response(status=200, text=product_json)
