import logging
from typing import Dict, TypeVar

T = TypeVar("T")


def match(object: T, query: Dict[str, str]):
    for key, value in query.items():
        logging.debug(f"Searching for {value} in {key}")

        if not hasattr(object, key):
            return False

        attr = getattr(object, key)
        if attr != value:
            return False

        logging.debug(f"Found {attr} in {key}")
    return True
