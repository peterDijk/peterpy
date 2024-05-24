import json
from typing import Any, Dict
from aiohttp.web import json_response as aiohttp_json_response

from peterpy.helpers import PeterPyEncoder


def json_response(status: int, content: Dict[str, Any], **kwargs):
    json_dump = json.dumps(content, cls=PeterPyEncoder)
    return aiohttp_json_response(status=status, text=json_dump, **kwargs)
