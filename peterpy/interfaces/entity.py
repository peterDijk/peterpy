from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Generic, List, TypeVar
from uuid import UUID

T = TypeVar("T")


@dataclass(kw_only=True, frozen=True)
class IEntity(ABC):
    @abstractmethod
    def to_json(self) -> Dict[str, Any]:
        raise NotImplementedError
