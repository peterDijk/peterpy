from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, TypeVar

T = TypeVar("T")


@dataclass(kw_only=True, frozen=True)
class IEntity(ABC):
    @abstractmethod
    def to_json(self) -> Dict[str, Any]:
        raise NotImplementedError
