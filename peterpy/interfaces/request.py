from aiohttp.web import Request, BaseRequest

from peterpy.services import ProductService


class PeterRequest(Request):
    product_service: ProductService | None = None

    def __init__(self, request: Request):
        super().__init__(
            request.message,
            request._payload,
            request.protocol,
            request._payload_writer,
            request.task,
            request.loop,
        )
