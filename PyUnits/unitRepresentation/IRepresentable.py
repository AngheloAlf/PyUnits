from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from ..TypesHelper import Number_t

class Representable(ABC):
    def copy(self):
        obj = super().__new__(self.getClass())
        for key, value in self.__dict__.items():
            if isinstance(value, list):
                obj.__dict__[key] = list(value)
            else:
                obj.__dict__[key] = value
        return obj

    def className(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def __hash__(self) -> int:
        raise NotImplementedError()
    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError()
    def __repr__(self) -> str:
        return self.__str__()


    @property
    @abstractmethod
    def numeratorUnits(self) -> List[Unit]:
        raise NotImplementedError()
    @property
    @abstractmethod
    def denominatorUnits(self) -> List[Unit]:
        raise NotImplementedError()

    @abstractmethod
    def hasSameUnit(self, other: Representable) -> bool:
        raise NotImplementedError()


    @abstractmethod
    def __eq__(self, other) -> bool:
        return False
    def __ne__(self, other) -> bool:
        return not self.__eq__(other)


    @abstractmethod
    def __mul__(self, other):
        if other is None:
            return self
        return NotImplemented
    @abstractmethod
    def __rmul__(self, other):
        if other is None:
            return self
        return NotImplemented

    @abstractmethod
    def __truediv__(self, other):
        if other is None:
            return self
        return NotImplemented
    @abstractmethod
    def __rtruediv__(self, other):
        return NotImplemented

    @abstractmethod
    def __floordiv__(self, other):
        if other is None:
            return self
        return NotImplemented
    @abstractmethod
    def __rfloordiv__(self, other):
        return NotImplemented

    @abstractmethod
    def __pow__(self, other: Number_t):
        if other is None:
            return self
        return NotImplemented

