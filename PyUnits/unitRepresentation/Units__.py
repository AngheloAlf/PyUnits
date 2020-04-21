from __future__ import annotations

from abc import ABC, abstractmethod
from numbers import Number, Complex, Real, Integral
from math import trunc, floor, ceil
from collections import Counter, Iterable
from typing import List, Tuple, Optional, Union, overload
from typing import SupportsInt, SupportsFloat, SupportsComplex

from ..TypesHelper import Number_t
from ..prefixes import SIPrefixes

from .UnitsInterfaces import SingleBaseUnitI, SingleUnitHandlerI, FractionUnitsI, ValueUnitsI
from .UnitsInterfaces import RepresentableI, UnitsI, SingleUnitI

class Unit(SingleBaseUnitI):
    def __new__(cls, unit: str):
        self = super().__new__(cls)

        self._unit = unit
        return self
    def __init__(self, unit: str):
        self._unit = self.unitName
    
    @property
    def unitName(self):
        return self._unit

    def __hash__(self):
        return hash(str(self))

    def __mul__(self, other):
        return super().__mul__(other)
    def __rmul__(self, other):
        return super().__rmul__(other)

    def __truediv__(self, other):
        return super().__truediv__(other)
    def __rtruediv__(self, other):
        return super().__rtruediv__(other)

    def __pow__(self, other: Number_t):
        return super().__pow__(other)

    def changePrefix(self, newPrefix: str) -> ValueUnitsI:
        unit = UnitHandler(self, newPrefix)
        exp = SIPrefixes.magnitudeFactor("", newPrefix)
        return ValueUnits(1, self, exp)


class UnitHandler(SingleUnitHandlerI):
    def __new__(cls, unit: SingleUnitI, prefix: str="", power: Number_t=1):
        self = super().__new__(cls)

        if isinstance(unit, SingleUnitHandlerI):
            raise NotImplementedError()

        self._baseUnit = unit
        self._prefix = prefix
        self._power = power
        return self
    def __init__(self, unit: SingleUnitI, prefix: str="", power: Number_t=1):
        self._baseUnit = self.baseUnit
        self._prefix = self.prefix
        self._power = self.power

    @property
    def baseUnit(self) -> SingleBaseUnitI:
        return self._baseUnit
    @property
    def prefix(self) -> str:
        return self._prefix
    @property
    def power(self) -> Number_t:
        return self._power

    def __hash__(self):
        return hash(str(self))

    def __mul__(self, other):
        if isinstance(other, SingleUnitI):
            if self.hasSameBaseAndPrefix(other):
                return UnitHandler(self.baseUnit, self.prefix, power=self.power+other.power)
            if self.baseUnit == other.baseUnit:
                baseunit = self.baseUnit
                prefix = self.prefix

                unit = UnitHandler(baseunit, prefix, self.power+other.power)
                value = SIPrefixes.magnitudeFactor(other.prefix, self.prefix)*other.power
                return ValueUnits(value, unit)
            
            return FractionUnits(self, other, divide=False)
        return super().__mul__(other)
    def __rmul__(self, other):
        return super().__rmul__(other)

    def __truediv__(self, other):
        return super().__truediv__(other)
    def __rtruediv__(self, other):
        return super().__rtruediv__(other)

    def __pow__(self, other: Number_t):
        return super().__pow__(other)

    def changePrefix(self, newPrefix: str) -> ValueUnitsI:
        unit = UnitHandler(self.baseUnit, newPrefix, self.power)
        if isinstance(self.power, (Integral, int)):
            exp = SIPrefixes.magnitudeFactor(self.prefix, newPrefix)*self.power
            return ValueUnits(1, unit, exp)
        else:
            value = 10**(SIPrefixes.magnitudeFactor(self.prefix, newPrefix)*self.power)
            return ValueUnits(value, unit)


class FractionUnits(FractionUnitsI):
    def __new__(cls, left: Union[UnitsI, Iterable, None], right: Optional[UnitsI]=None, *, divide: bool=True):
        self = super().__new__(cls)

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
                    if isinstance(unit, RepresentableI):
                        self._numerator += unit.numeratorUnits
                        self._denominator += unit.denominatorUnits
                else:
                    num2 = self.getBaseUnitFromNumerator(num)
                    if num2 is not None:
                        self._numerator.remove(num2)
                        unit = num*num2
                        if isinstance(unit, RepresentableI):
                            self._numerator += unit.numeratorUnits
                            self._denominator += unit.denominatorUnits
                    else:
                        self._numerator.append(num)

            for den in rightDen:
                num = self.getBaseUnitFromNumerator(den)
                if num is not None:
                    self._numerator.remove(num)
                    unit = num/den
                    if isinstance(unit, RepresentableI):
                        self._numerator += unit.numeratorUnits
                        self._denominator += unit.denominatorUnits
                else:
                    den2 = self.getBaseUnitFromDenominator(den)
                    if den2 is not None:
                        self._denominator.remove(den2)
                        unit = den*den2
                        if isinstance(unit, RepresentableI):
                            self._numerator += unit.denominatorUnits
                            self._denominator += unit.numeratorUnits
                    else:
                        self._denominator.append(den)


        if len(self._numerator) == 0 and len(self._denominator) == 0:
            raise NotImplementedError()

        return self

    def __init__(self, left: Union[UnitsI, Iterable, None], right: Optional[UnitsI]=None, *, divide: bool=True):
        self._numerator: List[SingleUnitI] = self.numeratorUnits
        self._denominator: List[SingleUnitI] = self.denominatorUnits

    @property
    def numeratorUnits(self) -> List[SingleUnitI]:
        return self._numerator
    @property
    def denominatorUnits(self) -> List[SingleUnitI]:
        return self._denominator

    def __hash__(self):
        return hash(str(self))

    def __mul__(self, other):
        return super().__mul__(other)
    def __rmul__(self, other):
        return super().__rmul__(other)

    def __truediv__(self, other):
        return super().__truediv__(other)
    def __rtruediv__(self, other):
        return super().__rtruediv__(other)

    def __pow__(self, other: Number_t):
        return super().__pow__(other)


class ValueUnits(ValueUnitsI):
    def __new__(cls, value, units: UnitsI, exp10: int=0):
        self = super(ValueUnits, cls).__new__(cls)

        if not isinstance(exp10, int):
            raise TypeError("Parameter `exp10` must be an int, not an " + type(exp10).__name__ + ".")

        self._value = value
        self._units = units
        self._exp10 = exp10
        return self

    def __init__(self, value, units: UnitsI, exp10: int=0):
        self._value = self.value
        self._units: UnitsI = self.units
        self._exp10: int = self.exp10

    @property
    def value(self):
        return self._value
    @property
    def units(self) -> UnitsI:
        return self._units
    @property
    def exp10(self) -> int:
        return self._exp10

    def __hash__(self):
        return hash(str(self))

    def __neg__(self) -> ValueUnitsI:
        raise NotImplementedError()
    def __pos__(self) -> ValueUnitsI:
        raise NotImplementedError()
    def __abs__(self) -> ValueUnitsI:
        raise NotImplementedError()

    def __round__(self, ndigits: int=0) -> ValueUnitsI:
        return NotImplemented
    def __trunc__(self) -> ValueUnitsI:
        return NotImplemented
    def __floor__(self) -> ValueUnitsI:
        return NotImplemented
    def __ceil__(self) -> ValueUnitsI:
        return NotImplemented


    def __add__(self, other: ValueUnitsI) -> ValueUnitsI:
        return NotImplemented
    def __radd__(self, other: ValueUnitsI) -> ValueUnitsI:
        return NotImplemented

    def __sub__(self, other: ValueUnitsI) -> ValueUnitsI:
        return NotImplemented
    def __rsub__(self, other: ValueUnitsI) -> ValueUnitsI:
        return NotImplemented

    def __mul__(self, other):
        return super().__mul__(other)
    def __rmul__(self, other):
        return super().__rmul__(other)

    def __truediv__(self, other):
        return super().__truediv__(other)
    def __rtruediv__(self, other):
        return super().__rtruediv__(other)

    def __floordiv__(self, other):
        return super().__truediv__(other)
    def __rfloordiv__(self, other):
        return super().__rtruediv__(other)

    def __pow__(self, other: Number_t):
        return super().__pow__(other)

    def __mod__(self, other) -> ValueUnitsI:
        return NotImplemented

