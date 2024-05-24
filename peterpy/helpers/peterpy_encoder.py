import json

from peterpy.interfaces.entity import IEntity


class PeterPyEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, IEntity):
            return o.to_json()
        return super().default(o)
