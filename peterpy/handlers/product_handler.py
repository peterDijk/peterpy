import logging
from uuid import UUID

from aiohttp.web import Request, Response

from peterpy import routes
from peterpy.helpers import json_response
from peterpy.interfaces import PeterRequest


@routes.get("/product/list")
async def list_products(request: Request) -> Response:
    # TODO: Can I extend `routes` to have a `PeterRequest` type?
    if not isinstance(request, PeterRequest):
        raise ValueError("Request is not a PeterRequest")

    logging.debug("---------------------------------")
    logging.info("List products requested from %s", request.remote)

    products = request.product_service.all()

    return json_response(
        status=200, content={"products": products, "count": len(products)}
    )


@routes.get("/product/{id}")
async def get_product(request: Request) -> Response:
    if not isinstance(request, PeterRequest):
        raise ValueError("Request is not a PeterRequest")

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


@routes.post("/product")
async def add_product(request: Request) -> Response:
    if not isinstance(request, PeterRequest):
        raise ValueError("Request is not a PeterRequest")

    logging.debug("---------------------------------")
    logging.info("Add product requested from %s", request.remote)

    data = await request.json()
    name = data.get("name")
    price = data.get("price")

    try:
        product = await request.product_service.add(name, price)
    except:
        raise ValueError("Failed to add product")

    return json_response(
        status=201,
        content={"product": product},
    )


# Add this to show adding batch of products, while only
# committing at the end of the batch in the middleware


@routes.post("/products/")
async def add_products(request: Request) -> Response:
    if not isinstance(request, PeterRequest):
        raise ValueError("Request is not a PeterRequest")

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


@routes.get("/")
async def get_dashboard(request: Request) -> Response:
    if not isinstance(request, PeterRequest):
        raise ValueError("Request is not a PeterRequest")

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
