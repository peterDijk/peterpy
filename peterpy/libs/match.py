from typing import Dict, TypeVar

T = TypeVar("T")


def match(obj: T, query: Dict[str, str]):
    for key, value in query.items():
        if not hasattr(obj, key):
            return False

        attr = getattr(obj, key)
        if attr != value:
            return False

    return True
