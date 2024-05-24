from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, TypeVar
from dataclasses import dataclass

from uuid import UUID

T = TypeVar("T")


@dataclass(kw_only=True, frozen=True)
class IEntity(ABC):
    @abstractmethod
    def to_json(self) -> Dict[str, Any]:
        raise NotImplementedError
