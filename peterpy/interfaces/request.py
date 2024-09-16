from aiohttp.web import BaseRequest, Request

from peterpy.services import ProductService


class PeterRequest(Request):
    product_service: ProductService

    def __init__(self, request: Request):
        super().__init__(
            request.message,
            request._payload,
            request.protocol,
            request._payload_writer,
            request.task,
            request.loop,
        )
