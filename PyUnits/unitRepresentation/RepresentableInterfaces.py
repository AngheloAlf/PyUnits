from __future__ import annotations

from abc import ABC, abstractmethod
from numbers import Number, Complex, Real, Integral
from math import trunc, floor, ceil
from collections import Counter, Iterable
from typing import List, Tuple, Optional, Union, overload
from typing import SupportsInt, SupportsFloat, SupportsComplex

from ..TypesHelper import Number_t
from ..prefixes import SIPrefixes


class RepresentableI(ABC):

    @property
    @abstractmethod
    def units(self) -> UnitsI:
        raise NotImplementedError()

    @property
    @abstractmethod
    def numeratorUnits(self) -> List[SingleUnitI]:
        raise NotImplementedError()
    @property
    @abstractmethod
    def denominatorUnits(self) -> List[SingleUnitI]:
        raise NotImplementedError()

    @property
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


    @abstractmethod
    def __eq__(self, other) -> bool:
        return False
    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __len__(self) -> int:
        return len(self.numeratorUnits) + len(self.denominatorUnits)


    @abstractmethod
    def __mul__(self, other):
        return NotImplemented
    @abstractmethod
    def __rmul__(self, other):
        return NotImplemented

    @abstractmethod
    def __truediv__(self, other):
        return NotImplemented
    @abstractmethod
    def __rtruediv__(self, other):
        return NotImplemented

    @abstractmethod
    def __floordiv__(self, other):
        return NotImplemented
    @abstractmethod
    def __rfloordiv__(self, other):
        return NotImplemented

    @abstractmethod
    def __pow__(self, other: Number_t):
        return NotImplemented

    @abstractmethod
    def hasSameUnits(self, other: RepresentableI) -> bool:
        raise NotImplementedError()
    @abstractmethod
    def hasSameBaseUnits(self, other: RepresentableI) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def containsUnit(self, other: SingleUnitI) -> bool:
        raise NotImplementedError()
    @abstractmethod
    def containsBaseUnit(self, other: SingleUnitI) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def containsUnitInNumerator(self, other: SingleUnitI) -> bool:
        raise NotImplementedError()
    @abstractmethod
    def containsBaseUnitInNumerator(self, other: SingleUnitI) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def containsUnitInDenominator(self, other: SingleUnitI) -> bool:
        raise NotImplementedError()
    @abstractmethod
    def containsBaseUnitInDenominator(self, other: SingleUnitI) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def getBaseUnitFromNumerator(self, other: SingleUnitI) -> Optional[SingleUnitI]:
        raise NotImplementedError()
    @abstractmethod
    def getBaseUnitFromDenominator(self, other: SingleUnitI) -> Optional[SingleUnitI]:
        raise NotImplementedError()

    def copy(self):
        obj = super().__new__(self.getClass())
        for key, value in self.__dict__.items():
            if isinstance(value, list):
                obj.__dict__[key] = list(value)
            else:
                obj.__dict__[key] = value
        return obj


class UnitsI(RepresentableI):

    @property
    def units(self) -> UnitsI:
        return self

    def __floordiv__(self, other):
        return self.__truediv__(other)
    def __rfloordiv__(self, other):
        return self.__rtruediv__(other)


class SingleUnitI(UnitsI):

    @property
    def numeratorUnits(self) -> List[SingleUnitI]:
        return [self]
    @property
    def denominatorUnits(self) -> List[SingleUnitI]:
        return []

    @property
    @abstractmethod
    def unitName(self) -> str:
        raise NotImplementedError()
    @property
    @abstractmethod
    def prefix(self) -> str:
        raise NotImplementedError()

    @property
    @abstractmethod
    def baseUnit(self) -> SingleUnitI:
        raise NotImplementedError()

    def __len__(self) -> int:
        return 1

    def containsUnitInDenominator(self, other: SingleUnitI) -> bool:
        return False
    def containsBaseUnitInDenominator(self, other: SingleUnitI) -> bool:
        return False
    def getBaseUnitFromDenominator(self, other: SingleUnitI) -> Optional[SingleUnitI]:
        return None

class SingleBaseUnitI(SingleUnitI):
    @property
    def baseUnit(self) -> SingleUnitI:
        return self

class SingleUnitHandlerI(SingleUnitI):
    @property
    def unitName(self) -> str:
        return self.baseUnit.unitName
    @property
    def prefix(self) -> str:
        return self.baseUnit.prefix

    @property
    @abstractmethod
    def power(self) -> Number_t:
        raise NotImplementedError()


class MultipleUnitsI(UnitsI):
    pass

class FractionUnitsI(MultipleUnitsI):
    pass


class RepValueUnitsI(RepresentableI, SupportsInt, SupportsFloat, SupportsComplex): 
    @property
    @abstractmethod
    def value(self):
        raise NotImplementedError()
    @property
    @abstractmethod
    def exp10(self) -> int:
        raise NotImplementedError()

    @abstractmethod
    def __neg__(self) -> RepValueUnitsI:
        raise NotImplementedError()
    @abstractmethod
    def __pos__(self) -> RepValueUnitsI:
        raise NotImplementedError()
    @abstractmethod
    def __abs__(self) -> RepValueUnitsI:
        raise NotImplementedError()

    @abstractmethod
    def __int__(self) -> int:
        raise NotImplementedError()
    @abstractmethod
    def __float__(self) -> float:
        raise NotImplementedError()
    @abstractmethod
    def __complex__(self) -> complex:
        raise NotImplementedError()

    @abstractmethod
    def __round__(self, ndigits: int=0) -> RepValueUnitsI:
        return NotImplemented
    @abstractmethod
    def __trunc__(self) -> RepValueUnitsI:
        return NotImplemented
    @abstractmethod
    def __floor__(self) -> RepValueUnitsI:
        return NotImplemented
    @abstractmethod
    def __ceil__(self) -> RepValueUnitsI:
        return NotImplemented

    @abstractmethod
    def __lt__(self, other) -> bool:
        if not isinstance(other, RepValueUnitsI):
            return NotImplemented
        return False
    @abstractmethod
    def __gt__(self, other) -> bool:
        if not isinstance(other, RepValueUnitsI):
            return NotImplemented
        return False

    def __le__(self, other) -> bool:
        if not isinstance(other, RepValueUnitsI):
            return NotImplemented
        return not self.__gt__(other)
    def __ge__(self, other) -> bool:
        if not isinstance(other, RepValueUnitsI):
            return NotImplemented
        return not self.__lt__(other)


    @abstractmethod
    def __add__(self, other: RepValueUnitI) -> RepValueUnitI:
        return NotImplemented
    @abstractmethod
    def __radd__(self, other: RepValueUnitI) -> RepValueUnitI:
        return NotImplemented

    @abstractmethod
    def __sub__(self, other: RepValueUnitI) -> RepValueUnitI:
        return NotImplemented
    @abstractmethod
    def __rsub__(self, other: RepValueUnitI) -> RepValueUnitI:
        return NotImplemented


    @abstractmethod
    def __mod__(self, other) -> RepValueUnitI:
        return NotImplemented

