from aiohttp.web import Request

from peterpy.services import ProductService


class PeterRequest(Request):
    product_service: ProductService
