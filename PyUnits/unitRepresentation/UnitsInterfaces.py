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

    def __repr__(self) -> str:
        return self.__str__()
    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError()
    @abstractmethod
    def __hash__(self) -> int:
        raise NotImplementedError()

    @abstractmethod
    def __eq__(self, other) -> bool:
        if not isinstance(other, RepresentableI):
            return NotImplemented
        return False
    def __ne__(self, other) -> bool:
        if not isinstance(other, RepresentableI):
            return NotImplemented
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


    def hasSameUnits(self, other: RepresentableI) -> bool:
        otherNum = other.numeratorUnits
        otherDen = other.denominatorUnits
        return Counter(self.numeratorUnits) == Counter(otherNum) and Counter(self.denominatorUnits) == Counter(otherDen)
    def hasSameBaseUnits(self, other: RepresentableI) -> bool:
        selfNum = map(lambda x: x.baseUnit, self.numeratorUnits)
        selfDen = map(lambda x: x.baseUnit, self.denominatorUnits)
        otherNum = map(lambda x: x.baseUnit, other.numeratorUnits)
        otherDen = map(lambda x: x.baseUnit, other.denominatorUnits)
        return Counter(selfNum) == Counter(otherNum) and Counter(selfDen) == Counter(otherDen)

    def containsUnit(self, other: SingleUnitI) -> bool:
        return self.containsUnitInNumerator(other) or self.containsUnitInDenominator(other)
    def containsBaseUnit(self, other: SingleUnitI) -> bool:
        return self.containsBaseUnitInNumerator(other) or self.containsBaseUnitInDenominator(other)

    def containsUnitInNumerator(self, other: SingleUnitI) -> bool:
        return self.getUnitFromNumerator(other) is not None
    def containsUnitInDenominator(self, other: SingleUnitI) -> bool:
        return self.getUnitFromDenominator(other) is not None

    def containsBaseUnitInNumerator(self, other: SingleUnitI) -> bool:
        return self.getBaseUnitFromNumerator(other) is not None
    def containsBaseUnitInDenominator(self, other: SingleUnitI) -> bool:
        return self.getBaseUnitFromDenominator(other) is not None

    def getUnitFromNumerator(self, other: SingleUnitI) -> Optional[SingleUnitI]:
        for unit in self.numeratorUnits:
            if unit.hasSameUnits(other):
                return unit
        return None
    def getUnitFromDenominator(self, other: SingleUnitI) -> Optional[SingleUnitI]:
        for unit in self.denominatorUnits:
            if unit.hasSameUnits(other):
                return unit
        return None

    def getBaseUnitFromNumerator(self, other: SingleUnitI) -> Optional[SingleUnitI]:
        for unit in self.numeratorUnits:
            if unit.hasSameBaseUnits(other):
                return unit
        return None
    def getBaseUnitFromDenominator(self, other: SingleUnitI) -> Optional[SingleUnitI]:
        for unit in self.denominatorUnits:
            if unit.hasSameBaseUnits(other):
                return unit
        return None

    @property
    def className(self) -> str:
        return self.__class__.__name__
    def copy(self):
        obj = super().__new__(self.__class__)
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
    def baseUnit(self) -> SingleBaseUnitI:
        raise NotImplementedError()
    @property
    @abstractmethod
    def prefix(self) -> str:
        raise NotImplementedError()
    @property
    @abstractmethod
    def power(self) -> Number_t:
        raise NotImplementedError()

    def __len__(self) -> int:
        return 1

    def containsUnitInDenominator(self, other: SingleUnitI) -> bool:
        return False
    def containsBaseUnitInDenominator(self, other: SingleUnitI) -> bool:
        return False
    def getUnitFromDenominator(self, other: SingleUnitI) -> Optional[SingleUnitI]:
        return None
    def getBaseUnitFromDenominator(self, other: SingleUnitI) -> Optional[SingleUnitI]:
        return None

    @abstractmethod
    def changePrefix(self, newPrefix: str) -> ValueUnitsI:
        raise NotImplementedError()

    def hasSameBaseAndPrefix(self, other: SingleUnitI) -> bool:
        return self == other and self.prefix == ""

class SingleBaseUnitI(SingleUnitI):
    @property
    def baseUnit(self) -> SingleBaseUnitI:
        return self
    @property
    def prefix(self) -> str:
        return ""
    @property
    def power(self) -> Number_t:
        return 1

    def __str__(self) -> str:
        return str(self.unitName)

    def __eq__(self, other):
        if not isinstance(other, SingleBaseUnitI):
            return super().__eq__(other)
        return self.unitName == other.unitName

class SingleUnitHandlerI(SingleUnitI):
    @property
    def unitName(self) -> str:
        return self.baseUnit.unitName
    def __str__(self) -> str:
        result = self.prefix + self.unitName
        if self.power != 1:
            return f"({result})^{self.power}"
        return result

    def __eq__(self, other):
        if not isinstance(other, SingleUnitHandlerI):
            return super().__eq__(other)
        return self.baseUnit == other.baseUnit and self.prefix == other.prefix and self.power == other.power


class MultipleUnitsI(UnitsI):
    def __str__(self) -> str:
        numList = list(map(str, self.numeratorUnits))
        aux = ""
        if len(numList) != 0:
            aux = "*".join(numList)
        else:
            aux = "1"
        if len(self.denominatorUnits) != 0:
            aux += "/"
            if len(self.denominatorUnits) == 1:
                aux += str(self.denominatorUnits[0])
            else:
                aux += "(" + "*".join(map(str, self.denominatorUnits)) + ")"
        return aux
    
    def __eq__(self, other):
        if not isinstance(other, MultipleUnitsI):
            return super().__eq__(other)
        otherNum = other.numeratorUnits
        otherDen = other.denominatorUnits
        return Counter(self.numeratorUnits) == Counter(otherNum) and Counter(self.denominatorUnits) == Counter(otherDen)


class FractionUnitsI(MultipleUnitsI):
    pass


class ValueUnitsI(RepresentableI, SupportsInt, SupportsFloat, SupportsComplex): 
    @property
    @abstractmethod
    def value(self):
        raise NotImplementedError()
    @property
    @abstractmethod
    def exp10(self) -> int:
        raise NotImplementedError()

    @property
    def numeratorUnits(self) -> List[SingleUnitI]:
        return self.units.numeratorUnits
    @property
    def denominatorUnits(self) -> List[SingleUnitI]:
        return self.units.denominatorUnits

    def __str__(self) -> str:
        result = str(self.value)
        if self.exp10 != 0:
            result += f"e{str(self.exp10)}"
        result += f" [{str(self.units)}]"
        return result

    @abstractmethod
    def __neg__(self) -> ValueUnitsI:
        raise NotImplementedError()
    @abstractmethod
    def __pos__(self) -> ValueUnitsI:
        raise NotImplementedError()
    @abstractmethod
    def __abs__(self) -> ValueUnitsI:
        raise NotImplementedError()

    def __int__(self) -> int:
        return int(self.value*(10**self.exp10))
    def __float__(self) -> float:
        return float(self.value*(10**self.exp10))
    def __complex__(self) -> complex:
        return complex(self.value*(10**self.exp10))

    @abstractmethod
    def __round__(self, ndigits: int=0) -> ValueUnitsI:
        return NotImplemented
    @abstractmethod
    def __trunc__(self) -> ValueUnitsI:
        return NotImplemented
    @abstractmethod
    def __floor__(self) -> ValueUnitsI:
        return NotImplemented
    @abstractmethod
    def __ceil__(self) -> ValueUnitsI:
        return NotImplemented

    def __eq__(self, other) -> bool:
        if not isinstance(other, ValueUnitsI):
            return NotImplemented
        return self.units == other.units and self.value*(10**self.exp10) == other.value*(10**other.exp10)

    def __lt__(self, other) -> bool:
        if not isinstance(other, ValueUnitsI):
            return NotImplemented
        if not self.hasSameUnits(other):
            return NotImplemented
        return self.value*(10**self.exp10) < other.value*(10**other.exp10)
    def __gt__(self, other) -> bool:
        if not isinstance(other, ValueUnitsI):
            return NotImplemented
        if not self.hasSameUnits(other):
            return NotImplemented
        return self.value*(10**self.exp10) > other.value*(10**other.exp10)

    def __le__(self, other) -> bool:
        if not isinstance(other, ValueUnitsI):
            return NotImplemented
        if not self.hasSameUnits(other):
            return NotImplemented
        return not self.__gt__(other)
    def __ge__(self, other) -> bool:
        if not isinstance(other, ValueUnitsI):
            return NotImplemented
        if not self.hasSameUnits(other):
            return NotImplemented
        return not self.__lt__(other)


    @abstractmethod
    def __add__(self, other: ValueUnitsI) -> ValueUnitsI:
        return NotImplemented
    @abstractmethod
    def __radd__(self, other: ValueUnitsI) -> ValueUnitsI:
        return NotImplemented

    @abstractmethod
    def __sub__(self, other: ValueUnitsI) -> ValueUnitsI:
        return NotImplemented
    @abstractmethod
    def __rsub__(self, other: ValueUnitsI) -> ValueUnitsI:
        return NotImplemented

    @abstractmethod
    def __mod__(self, other) -> ValueUnitsI:
        return NotImplemented

