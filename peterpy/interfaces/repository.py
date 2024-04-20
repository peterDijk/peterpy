from abc import ABC, abstractmethod
from typing import Dict, List, TypeVar, Generic
from uuid import UUID

T = TypeVar("T")


class IRepository(Generic[T]):  # ABC need the commit etc methods
    items: Dict[UUID, T]

    @abstractmethod
    def get(self, _id: UUID) -> T:
        raise NotImplementedError

    @abstractmethod
    def add(self, obj: T) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, obj: T) -> None:
        raise NotImplementedError

    @abstractmethod
    def remove(self, obj: T) -> None:
        raise NotImplementedError

    @abstractmethod
    def find(self, query: Dict[str, T]) -> List[T]:
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

    # @abstractmethod
    # # find out how to implement this
    # def commit(self) -> None:
    #     pass

    # @abstractmethod
    # # find out how to implement this
    # def rollback(self) -> None:
    #     pass

    # @abstractmethod
    # # find out how to implement this
    # def close(self) -> None:
    #     pass

    # @abstractmethod
    # # find out what these should do
    # def __enter__(self) -> "IRepository":
    #     pass

    # @abstractmethod
    # # find out what these should do
    # def __exit__(self, exc_type, exc_value, traceback) -> None:
    #     pass
