import logging
from uuid import UUID

from aiohttp.web import Request, Response

from peterpy.helpers import json_response
from peterpy.services.product_service import ProductService


async def list_products(request: Request) -> Response:
    product_service: ProductService = request["product_service"]

    logging.debug("---------------------------------")
    logging.info("List products requested from %s", request.remote)

    page = int(request.query.get("page", 1))
    limit = int(request.query.get("limit", 20))

    # converting the products to a list here
    # removes the memory advantage of using a generator
    # really using the benefits of a generator would be to use it
    # in the json encoder, which would then iterate over the generator
    # and stream the response items one by one back to the client

    # TODO: investigate how to stream the response item by item back to the client
    products = list(product_service.all(page, limit))

    return json_response(status=200, content={"products": products})


async def get_product(request: Request) -> Response:
    product_service: ProductService = request["product_service"]

    logging.debug("---------------------------------")
    logging.info("Get one product requested from %s", request.remote)

    try:
        product_id = UUID(request.match_info["id"])
    except ValueError:
        return json_response(status=400, content={"error": "Invalid UUID"})

    try:
        product = product_service.get(product_id)
    except KeyError as e:
        return json_response(status=404, content={"error": str(e)})

    return json_response(status=200, content={"product": product})


async def add_product(request: Request) -> Response:
    try:
        product_service: ProductService = request["product_service"]

        logging.debug("---------------------------------")
        logging.info("Add product requested from %s", request.remote)

        data = await request.json()
        name = data.get("name")
        price = data.get("price")

        product = await product_service.add(name, price)

        return json_response(
            status=201,
            content={"product": product},
        )
    except ValueError as e:
        return json_response(status=500, content={"error": str(e)})


# Add this to show adding batch of products, while only
# committing at the end of the batch in the middleware
async def add_products(request: Request) -> Response:
    product_service: ProductService = request["product_service"]

    logging.debug("---------------------------------")
    logging.info("Add multiple products requested from %s", request.remote)

    data = await request.json()
    products = data.get("products")

    for product in products:
        name = product.get("name")
        price = product.get("price")
        product = await product_service.add(name, price)

    return json_response(status=201, content={"products": products})


async def get_dashboard(request: Request) -> Response:
    product_service: ProductService = request["product_service"]

    logging.debug("---------------------------------")
    logging.info("Dashboard requested from %s", request.remote)

    products_count = product_service.count()
    products_sum = product_service.sum()

    output = {
        "products_count": products_count,
        "products_total_value": products_sum,
    }

    return json_response(status=200, content={"dashboard": output})
