from abc import ABC, abstractmethod
from typing import Dict, Generator, Generic, List, TypeVar
from uuid import UUID

T = TypeVar("T")


# class IRepository(Generic[T], metaclass=ABCMeta):
class IRepository(ABC, Generic[T]):
    items: Dict[UUID, T]

    @abstractmethod
    def get(self, _id: UUID) -> T:
        raise NotImplementedError

    @abstractmethod
    def add(self, obj: T, flush: bool) -> T:
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
    def find_one(self, obj_id: UUID) -> T:
        raise NotImplementedError

    @abstractmethod
    def all(self, page: int, limit: int) -> Generator[T, None, None]:
        raise NotImplementedError

    @abstractmethod
    def count(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def clear(self) -> None:
        pass
