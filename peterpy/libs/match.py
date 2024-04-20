import logging
from typing import Dict, TypeVar

T = TypeVar("T")


def match(object: T, query: Dict[str, str]):
    for key, value in query.items():
        if not hasattr(object, key):
            return False

        attr = getattr(object, key)
        if attr != value:
            return False

    return True
