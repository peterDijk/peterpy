from abc import ABC, ABCMeta, abstractmethod
from typing import Dict, Generic, List, TypeVar
from uuid import UUID

T = TypeVar("T")


# class IRepository(Generic[T], metaclass=ABCMeta):
class IRepository(ABC, Generic[T]):
    items: Dict[UUID, T]

    @abstractmethod
    def get(self, _id: UUID) -> T:
        raise NotImplementedError

    @abstractmethod
    def add(self, obj: T) -> T:
        raise NotImplementedError

    @abstractmethod
    def update(self, obj: T) -> T:
        raise NotImplementedError

    @abstractmethod
    def remove(self, obj: T) -> T:
        raise NotImplementedError

    @abstractmethod
    def find(self, query: Dict[str, str]) -> List[T]:
        raise NotImplementedError

    @abstractmethod
    def find_one(self, _id: UUID) -> T:
        raise NotImplementedError

    @abstractmethod
    def all(self) -> List[T]:
        raise NotImplementedError

    @abstractmethod
    def count(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def clear(self) -> None:
        pass
