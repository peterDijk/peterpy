import json
import logging
from uuid import UUID

from aiohttp.web import Request, Response, json_response

from peterpy import routes
from peterpy.entities import ProductEncoder
from peterpy.repositories import MemoryProductRepository, DatabaseProductRepository
from peterpy.services import ProductService

# define globally because we are using a memory repository
# every method of the service will use the same repository
memory_product_repository = MemoryProductRepository()


@routes.get("/list")
async def list_products(request: Request) -> Response:
    logging.debug("---------------------------------")
    logging.info("List products requested from %s", request.remote)

    database_product_repository = DatabaseProductRepository()
    product_service = ProductService(database_product_repository)
    products = product_service.all()
    products_count = product_service.count()

    product_json = json.dumps(
        {"products": products, "count": products_count}, cls=ProductEncoder
    )

    return json_response(status=200, text=product_json)


@routes.get("/product/{id}")
async def get_product(request: Request) -> Response:
    logging.debug("---------------------------------")
    logging.info("Get one product requested from %s", request.remote)

    product_service = ProductService(memory_product_repository)
    try:
        product_id = UUID(request.match_info["id"])
    except ValueError:
        return json_response(status=400, text=json.dumps({"error": "Invalid UUID"}))

    try:
        product = product_service.get(product_id)
    except KeyError as e:
        return json_response(status=404, text=json.dumps({"error": str(e)}))

    return json_response(
        status=200,
        text=json.dumps({"product": product}, cls=ProductEncoder),
    )


@routes.post("/product")
async def add_product(request: Request) -> Response:
    logging.debug("---------------------------------")
    logging.info("Add product requested from %s", request.remote)

    data = await request.json()
    name = data.get("name")
    price = data.get("price")

    database_product_repository = DatabaseProductRepository()
    product_service = ProductService(database_product_repository)

    try:
        product = product_service.add(name, price)
    except ValueError as e:
        return json_response(status=400, text=json.dumps({"error": str(e)}))

    return json_response(
        status=201,
        text=json.dumps({"message": "Product added", "product_name": product.name}),
    )


@routes.get("/")
async def get_dashboard(request: Request) -> Response:
    logging.debug("---------------------------------")
    logging.info("Dashboard requested from %s", request.remote)

    database_product_repository = DatabaseProductRepository()
    product_service = ProductService(database_product_repository)
    products_count = product_service.count()
    products = product_service.all()
    products_total_value = sum([product.price for product in products])

    output = {
        "products_count": products_count,
        "products_total_value": products_total_value,
    }

    return json_response(status=200, text=json.dumps({"dashboard": output}))
