import logging
import json

from aiohttp.web import Request, Response, json_response

from peterpy import routes
from peterpy.repositories import MemoryProductRepository
from peterpy.services import ProductService

product_repository = MemoryProductRepository()


@routes.get("/list")
async def list_products(request: Request) -> Response:
    logging.info("List products requested from %s", request.remote)

    product_service = ProductService(product_repository)
    products = product_service.all()
    products_count = product_service.count()

    product_json = json.dumps({"products": products, "count": products_count})

    return json_response(status=200, text=product_json)


@routes.post("/add")
async def add_product(request: Request) -> Response:
    logging.info("Add product requested from %s", request.remote)

    data = await request.json()
    name = data.get("name")
    price = data.get("price")

    product_service = ProductService(product_repository)
    product = product_service.add(name, price)

    return json_response(
        status=201,
        text=json.dumps({"message": "Product added", "product_name": product.name}),
    )
