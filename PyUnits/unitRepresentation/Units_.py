from __future__ import annotations

from abc import ABC, abstractmethod
from numbers import Number, Complex, Real, Integral
from math import trunc, floor, ceil
from collections import Counter, Iterable
from typing import List, Tuple, Optional, Union, overload
from typing import SupportsInt, SupportsFloat, SupportsComplex

from ..TypesHelper import Number_t
from ..prefixes import SIPrefixes
from .RepresentableInterfaces import SingleBaseUnitI, SingleUnitHandlerI
from .RepresentableInterfaces import FractionUnitsI

from .RepresentableInterfaces import UnitsI, SingleUnitI, MultipleUnitsI


class BaseUnit(SingleBaseUnitI):

    def __new__(cls, unit: str, prefix: str=""):
        self = super().__new__(cls)

        #if not isinstance(unit, str):
        #    raise TypeError(f"Expected type str for 'unit', not {type(unit).__name__}.")
        #if not isinstance(defaultPrefix, str):
        #    raise TypeError(f"Expected type str for 'defaultPrefix', not {type(defaultPrefix).__name__}.")
        #if not SIPrefixes.isValidPrefix(prefix):
        #    raise TypeError(f"Invalid prefix: {defaultPrefix}.")

        self._unit = unit
        self._prefix = prefix
        return self

    def __init__(self, unit: str, prefix: str=""):
        self._unit: str = self.unitName
        self._prefix: str = self.prefix

    @property
    def unitName(self) -> str:
        return self._unit
    @property
    def prefix(self) -> str:
        return self._prefix


    def __hash__(self) -> int:
        return hash(str())

    def __str__(self) -> str:
        return self.prefix + self.unitName


    def __eq__(self, other) -> bool:
        if isinstance(other, BaseUnit):
            return self.unitName == other.unitName and self.prefix == other.prefix
        return super().__eq__(other)


    def __mul__(self, other):
        return NotImplemented

    def __rmul__(self, other):
        return NotImplemented


    def __truediv__(self, other):
        return NotImplemented

    def __rtruediv__(self, other):
        return NotImplemented


    def __pow__(self, other: Number_t):
        if isinstance(other, Number):
            if other == 1:
                return self
            return UnitHandler(self.baseUnit, power=other)
        return super().__pow__(other)



    def hasSameUnits(self, other: RepresentableI) -> bool:
        return self == other
    def hasSameBaseUnits(self, other: RepresentableI) -> bool:
        if isinstance(other, BaseUnit):
            return self == other
        return other.hasSameBaseUnits(self)

    def containsUnit(self, other: SingleUnitI) -> bool:
        return self == other
    def containsBaseUnit(self, other: SingleUnitI) -> bool:
        raise NotImplementedError()

    def containsUnitInNumerator(self, other: SingleUnitI) -> bool:
        return self == other
    def containsBaseUnitInNumerator(self, other: SingleUnitI) -> bool:
        raise NotImplementedError()

    def getBaseUnitFromNumerator(self, other: SingleUnitI) -> Optional[SingleUnitI]:
        raise NotImplementedError()
    def getBaseUnitFromDenominator(self, other: SingleUnitI) -> Optional[SingleUnitI]:
        raise NotImplementedError()


class UnitHandler(SingleUnitHandlerI):
    def __new__(cls, unit: SingleUnitI, power: Number_t=1):
        self = super().__new__(cls)

        #if not isinstance(unit, SingleUnitI):
        #    raise TypeError(f"Expected type str for 'unit', not {type(unit).__name__}.")
        #if not isinstance(power, Number):
        #    raise TypeError(f"Expected a numeral type for power, not {type(power).__name__}.")

        if isinstance(unit, SingleUnitHandlerI):
            raise NotImplementedError()

        if power == 0:
            return 1
        elif isinstance(power, Real) and power < 0:
            return FractionUnits(None, UnitHandler(unit, power=-power), divide=True)
            # raise NotImplementedError()

        self._baseUnit = unit
        self._power = power

        return self

    def __init__(self, unit: SingleUnitI, power: Number_t=1):
        self._baseUnit: SingleUnitI = self.baseUnit
        self._power: Number_t = self.power

    @property
    def baseUnit(self) -> SingleUnitI:
        return self._baseUnit
    @property
    def power(self) -> Number_t:
        return self._power

    def __hash__(self) -> int:
        return hash(str())
    def __str__(self) -> str:
        if self.power != 1:
            return f"({str(self.baseUnit)})^{self.power}"
        return str(self.baseUnit)

    def __eq__(self, other) -> bool:
        if isinstance(other, SingleUnitHandlerI):
            return self.power == other.power and self.baseUnit == other.baseUnit
        if isinstance(other, SingleBaseUnitI):
            return self.power == 1 and self.baseUnit == other
        return super().__eq__(other)

    def __mul__(self, other):
        if self.hasSameBaseUnits(other):
            if isinstance(other, SingleBaseUnitI):
                return UnitHandler(self.baseUnit, self.power+1)
            elif isinstance(other, SingleUnitHandlerI):
                return UnitHandler(self.baseUnit, self.power+other.power)
            else:
                return NotImplemented
        if isinstance(other, UnitsI):
            return FractionUnits(self, other, divide=False)
        return super().__mul__(other)
    def __rmul__(self, other):
        if self.hasSameBaseUnits(other):
            if isinstance(other, SingleBaseUnitI):
                return UnitHandler(self.baseUnit, self.power+1)
            elif isinstance(other, SingleUnitHandlerI):
                return UnitHandler(self.baseUnit, self.power+other.power)
            else:
                return NotImplemented
        if isinstance(other, UnitsI):
            return FractionUnits(other, self, divide=False)
        return super().__rmul__(other)

    def __truediv__(self, other):
        if self.hasSameBaseUnits(other):
            if isinstance(other, SingleBaseUnitI):
                return UnitHandler(self.baseUnit, self.power-1)
            elif isinstance(other, SingleUnitHandlerI):
                return UnitHandler(self.baseUnit, self.power-other.power)
            else:
                return NotImplemented
        if isinstance(other, UnitsI):
            return FractionUnits(self, other, divide=True)
        return super().__mul__(other)
    def __rtruediv__(self, other):
        if self.hasSameBaseUnits(other):
            if isinstance(other, SingleBaseUnitI):
                return UnitHandler(self.baseUnit, 1-self.power)
            elif isinstance(other, SingleUnitHandlerI):
                return UnitHandler(self.baseUnit, other.power-self.power)
            else:
                return NotImplemented
        if isinstance(other, UnitsI):
            return FractionUnits(other, self, divide=True)
        return super().__mul__(other)

    def __pow__(self, other: Number_t):
        if isinstance(other, Number):
            if other == 1:
                return self
            return UnitHandler(self.baseUnit, power=self.power*other)
        return super().__pow__(other)

    def hasSameUnits(self, other: RepresentableI) -> bool:
        raise NotImplementedError()
    def hasSameBaseUnits(self, other: RepresentableI) -> bool:
        if isinstance(other, SingleUnitHandlerI):
            return self.baseUnit == other.baseUnit
        return self.baseUnit == other

    def containsUnit(self, other: SingleUnitI) -> bool:
        raise NotImplementedError()
    def containsBaseUnit(self, other: SingleUnitI) -> bool:
        raise NotImplementedError()

    def containsUnitInNumerator(self, other: SingleUnitI) -> bool:
        raise NotImplementedError()
    def containsBaseUnitInNumerator(self, other: SingleUnitI) -> bool:
        raise NotImplementedError()

    def getBaseUnitFromNumerator(self, other: SingleUnitI) -> Optional[SingleUnitI]:
        raise NotImplementedError()
    def getBaseUnitFromDenominator(self, other: SingleUnitI) -> Optional[SingleUnitI]:
        raise NotImplementedError()



class FractionUnits(FractionUnitsI):

    def __new__(cls, left: Union[UnitsI, Iterator], right: Optional[UnitsI]=None, divide: bool=True):
        self: FractionUnits = super().__new__(cls)

        self._numerator = list()
        self._denominator = list()

        if isinstance(left, Iterable):
            self._numerator = list(left)
        elif left is not None:
            self._numerator = list(left.numeratorUnits)
            self._denominator = list(left.denominatorUnits)

        if right is not None:
            rightNum = right.numeratorUnits
            rightDen = right.denominatorUnits
            if divide:
                rightNum, rightDen = rightDen, rightNum

            for num in rightNum:
                den = self.getBaseUnitFromDenominator(num)
                if den is not None:
                    self._denominator.remove(den)
                    unit = num/den
                    if isinstance(unit, UnitsI):
                        self._numerator += unit.numeratorUnits
                        self._denominator += unit.denominatorUnits
                else:
                    num2 = self.getBaseUnitFromNumerator(num)
                    if num2 is not None:
                        self._numerator.remove(num2)
                        unit = num*num2
                        if isinstance(unit, UnitsI):
                            self._numerator += unit.numeratorUnits
                            self._denominator += unit.denominatorUnits
                    else:
                        self._numerator.append(num)

            for den in rightDen:
                num = self.getBaseUnitFromNumerator(den)
                if num is not None:
                    self._numerator.remove(num)
                    unit = num/den
                    if isinstance(unit, UnitsI):
                        self._numerator += unit.numeratorUnits
                        self._denominator += unit.denominatorUnits
                else:
                    den2 = self.getBaseUnitFromDenominator(den)
                    if den2 is not None:
                        self._denominator.remove(den2)
                        unit = den*den2
                        if isinstance(unit, UnitsI):
                            self._numerator += unit.denominatorUnits
                            self._denominator += unit.numeratorUnits
                    else:
                        self._denominator.append(den)

        if len(self._numerator) == 0 and len(self._denominator) == 0:
            raise NotImplementedError()

        return self

    def __init__(self, left: Union[UnitsI, Iterator], right: Optional[UnitsI]=None, divide: bool=True):
        self._numerator: List[SingleUnitI] = self._numerator
        self._denominator: List[SingleUnitI] = self._denominator

    @property
    def numeratorUnits(self) -> List[SingleUnitI]:
        return list(self._numerator)
    @property
    def denominatorUnits(self) -> List[SingleUnitI]:
        return list(self._denominator)

    def __hash__(self) -> int:
        return hash(str(self))
    def __str__(self) -> str:
        numList = list(map(str, self.numeratorUnits))
        aux = ""
        if len(self.numeratorUnits) != 0:
            aux = "*".join(numList)
        else:
            aux = "1"
        if len(self.denominatorUnits) != 0:
            aux += "/"
            if len(self.denominatorUnits) == 1:
                aux += str(self.denominatorUnits[0])
            else:
                denList = list(map(str, self.denominatorUnits))
                aux += "(" + "*".join(denList) + ")"
        return aux

    def __eq__(self, other) -> bool:
        raise NotImplementedError()

    def __mul__(self, other):
        return NotImplemented
    def __rmul__(self, other):
        return NotImplemented

    def __truediv__(self, other):
        return NotImplemented
    def __rtruediv__(self, other):
        return NotImplemented

    def __pow__(self, other: Number_t):
        if isinstance(other, Number):
            numerator = list()
            denominator = list()
            for num in self.numeratorUnits:
                numerator.append(num**other)
            for den in self.denominatorUnits:
                denominator.append(den**other)
            return FractionUnits(numerator, divide=False) / FractionUnits(denominator, divide=False)
        return super().__pow__(other)


    def hasSameUnits(self, other: RepresentableI) -> bool:
        raise NotImplementedError()
    def hasSameBaseUnits(self, other: RepresentableI) -> bool:
        raise NotImplementedError()

    def containsUnit(self, other: SingleUnitI) -> bool:
        return self.containsUnitInNumerator(other) or self.containsUnitInDenominator(other)
    def containsBaseUnit(self, other: SingleUnitI) -> bool:
        raise NotImplementedError()

    def containsUnitInNumerator(self, other: SingleUnitI) -> bool:
        raise NotImplementedError()
    def containsBaseUnitInNumerator(self, other: SingleUnitI) -> bool:
        return self.getBaseUnitFromNumerator(other) is not None

    def containsUnitInDenominator(self, other: SingleUnitI) -> bool:
        raise NotImplementedError()
    def containsBaseUnitInDenominator(self, other: SingleUnitI) -> bool:
        return self.getBaseUnitFromDenominator(other) is not None

    def getBaseUnitFromNumerator(self, other: SingleUnitI) -> Optional[SingleUnitI]:
        for num in self._numerator:
            if num.hasSameBaseUnits(other):
                return num
        return None
    def getBaseUnitFromDenominator(self, other: SingleUnitI) -> Optional[SingleUnitI]:
        for den in self._denominator:
            if den.hasSameBaseUnits(other):
                return den
        return None




class RepValueUnits(RepValueUnitsI):
    pass

