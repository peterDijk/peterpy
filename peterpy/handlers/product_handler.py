import logging
from uuid import UUID

from aiohttp.web import Request, Response

from peterpy.services import ProductService
from peterpy.services import ProductService

from peterpy.helpers import json_response


class PeterRequest(Request):
    product_service: ProductService


async def list_products(request: PeterRequest) -> Response:
    logging.debug("---------------------------------")
    logging.info("List products requested from %s", request.remote)

    products = request.product_service.all()

    return json_response(
        status=200, content={"products": products, "count": len(products)}
    )


async def get_product(request: PeterRequest) -> Response:
    logging.debug("---------------------------------")
    logging.info("Get one product requested from %s", request.remote)

    try:
        product_id = UUID(request.match_info["id"])
    except ValueError:
        return json_response(status=400, content={"error": "Invalid UUID"})

    try:
        product = request.product_service.get(product_id)
    except KeyError as e:
        return json_response(status=404, content={"error": str(e)})

    return json_response(status=200, content={"product": product})


async def add_product(request: PeterRequest) -> Response:
    logging.debug("---------------------------------")
    logging.info("Add product requested from %s", request.remote)

    data = await request.json()
    name = data.get("name")
    price = data.get("price")

    try:
        product = await request.product_service.add(name, price)
    except ValueError as e:
        return json_response(status=400, content={"error": str(e)})

    return json_response(
        status=201,
        content={"product": product},
    )


# Add this to show adding batch of products, while only
# committing at the end of the batch in the middleware


async def add_products(request: PeterRequest) -> Response:
    logging.debug("---------------------------------")
    logging.info("Add multiple products requested from %s", request.remote)

    data = await request.json()
    products = data.get("products")

    try:
        for product in products:
            name = product.get("name")
            price = product.get("price")
            product = await request.product_service.add(name, price)

        return json_response(status=201, content={"products": products})
    except:
        raise ValueError("1 or more products failed to add")


# @routes.get("/")
async def get_dashboard(request: PeterRequest) -> Response:
    logging.debug("---------------------------------")
    logging.info("Dashboard requested from %s", request.remote)

    products_count = request.product_service.count()
    products = request.product_service.all()
    products_total_value = sum([product.price for product in products])

    output = {
        "products_count": products_count,
        "products_total_value": products_total_value,
    }

    return json_response(status=200, content={"dashboard": output})
