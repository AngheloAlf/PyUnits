from __future__ import annotations

from abc import ABC, abstractmethod
from numbers import Number
from math import trunc, floor, ceil
from collections import Counter, Iterable
from typing import List, Tuple, Optional, Union

from ..prefixes import SIPrefixes


class RepresentableUnit(ABC):
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
    def __str__(self) -> str:
        pass

    def __repr__(self) -> str:
        return self.__str__()


    @abstractmethod
    def getUnitsLists(self) -> Tuple[UnitsList_t, UnitsList_t]:
        pass

    @abstractmethod
    def hasSameUnit(self, other) -> bool:
        pass


    @abstractmethod
    def __eq__(self, other) -> bool:
        pass
    @abstractmethod
    def __ne__(self, other) -> bool:
        pass


    @abstractmethod
    def __mul__(self, other):
        if isinstance(other, Number):
            return ValueUnits(other, self)
        if other is None:
            return self
        return NotImplemented

    @abstractmethod
    def __rmul__(self, other):
        if isinstance(other, Number):
            return ValueUnits(other, self)
        if other is None:
            return self
        return NotImplemented


    @abstractmethod
    def __truediv__(self, other):
        if isinstance(other, Number):
            return ValueUnits(1/other, self)
        if other is None:
            return self
        return NotImplemented

    @abstractmethod
    def __rtruediv__(self, other):
        if isinstance(other, Number):
            return ValueUnits(other, UnitsFraction(None, self, divide=True))
        if other is None:
            return UnitsFraction(None, self, divide=True)
        return NotImplemented


    @abstractmethod
    def __pow__(self, other: Number):
        return NotImplemented


class Unit(RepresentableUnit):

    # attributes:
    # self._unit: str
    # self._defaultPrefix: str
    # self._power: Number

    # inmutable

    def __new__(cls, unit: str, defaultPrefix: str="", *, power: Number=1):
        assert(isinstance(unit, str))
        assert(isinstance(defaultPrefix, str))
        assert(isinstance(power, Number))
        assert(SIPrefixes.isValidPrefix(defaultPrefix))
        self = super(Unit, cls).__new__(cls)

        if power == 0:
            return 1
        elif power < 0:
            return UnitsFraction(None, Unit(unit, defaultPrefix, power=-power), divide=True)

        return self

    def __init__(self, unit: str, defaultPrefix: str="", *, power: Number=1):
        self._unit: str = unit
        self._defaultPrefix: str = defaultPrefix
        self._power: Number = power

    def __hash__(self) -> int:
        return hash(str(self))

    def __str__(self) -> str:
        if self._power != 1:
            return f"({self._defaultPrefix}{self._unit}^{self._power})"
        return self._defaultPrefix + self._unit


    @property
    def unit(self) -> str:
        return self._unit

    @property
    def defaultPrefix(self) -> str:
        return self._defaultPrefix

    @property
    def power(self) -> Number:
        return self._power


    def getUnitsLists(self) -> Tuple[UnitsList_t, UnitsList_t]:
        return ([self], [])

    def hasSameUnit(self, other) -> bool:
        otherNum, otherDen = other.getUnitsLists()
        if len(otherDen) != 0:
            return False
        if len(otherNum) != 1:
            return False
        return self._unit == otherNum[0]._unit and self._defaultPrefix == otherNum[0]._defaultPrefix and self._power == otherNum[0]._power

    def hasSameBaseUnit(self, other) -> bool:
        otherNum, otherDen = other.getUnitsLists()
        if len(otherDen) != 0:
            return False
        if len(otherNum) != 1:
            return False
        return self._unit == otherNum[0]._unit and self._defaultPrefix == otherNum[0]._defaultPrefix

    def __eq__(self, other) -> bool:
        if isinstance(other, Number):
            return False
        otherNum, otherDen = other.getUnitsLists()
        if len(otherDen) != 0:
            return False
        if len(otherNum) != 1:
            return False
        if self._unit != otherNum[0]._unit:
            return False
        if self._defaultPrefix != otherNum[0]._defaultPrefix:
            return False
        if self._power != otherNum[0]._power:
            return False
        return True

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)


    def __mul__(self, other):
        if isinstance(other, Unit) and self.hasSameBaseUnit(other):
            return Unit(self._unit, self._defaultPrefix, power=self._power+other._power)

        if isinstance(other, (Unit, UnitsFraction)):
            return UnitsFraction(self, other, divide=False)

        return super().__mul__(other)

    def __rmul__(self, other):
        if isinstance(other, Unit) and self.hasSameBaseUnit(other):
            return Unit(self._unit, self._defaultPrefix, power=other._power+self._power)

        if isinstance(other, (Unit, UnitsFraction)):
            return UnitsFraction(other, self, divide=False)

        return super().__rmul__(other)


    def __truediv__(self, other):
        if isinstance(other, Unit) and self.hasSameBaseUnit(other):
            return Unit(self._unit, self._defaultPrefix, power=self._power-other._power)

        if isinstance(other, (Unit, UnitsFraction)):
            return UnitsFraction(self, other, divide=True)

        return super().__truediv__(other)

    def __rtruediv__(self, other):
        if isinstance(other, Unit) and self.hasSameBaseUnit(other):
            return Unit(self._unit, self._defaultPrefix, power=other._power-self._power)

        if isinstance(other, (Unit, UnitsFraction)):
            return UnitsFraction(other, self, divide=True)

        return super().__rtruediv__(other)


    def __pow__(self, other: Number) -> Unit:
        if isinstance(other, Number):
            if other == 1:
                return self
            return Unit(self._unit, self._defaultPrefix, power=self._power*other)

        return super().__pow__(other)

UnitsList_t = List[Unit]


class UnitsFraction(RepresentableUnit):

    # attributes:
    # self._numerator: UnitsList_t
    # self._denominator: UnitsList_t

    # inmutable

    def __new__(cls, left: Union[RepresentableUnit, Iterable, None], right: Union[RepresentableUnit, Iterable, None]=None, *, divide: bool):
        assert(isinstance(left, (RepresentableUnit, Iterable, type(None))))
        assert(isinstance(right, (RepresentableUnit, Iterable, type(None))))
        assert(isinstance(divide, bool))
        self = super(UnitsFraction, cls).__new__(cls)

        self._numerator = list()
        self._denominator = list()

        if isinstance(left, Iterable):
            self._numerator = list(left)
        elif left is not None:
            leftNum, leftDen = left.getUnitsLists()
            self._numerator = list(leftNum)
            self._denominator = list(leftDen)

        if isinstance(right, Iterable):
            raise TypeError("`right` parameter can't be Iterable.")
        elif right is not None:
            rightNum, rightDen = right.getUnitsLists()
            if divide:
                rightNum, rightDen = rightDen, rightNum

            for num in rightNum:
                den = self.unitInDenominator(num)
                if den is not None:
                    self._denominator.remove(den)
                    unit = num/den
                    if isinstance(unit, (Unit, UnitsFraction)):
                        numList, denList = unit.getUnitsLists()
                        self._numerator += numList
                        self._denominator += denList

                else:
                    num2 = self.unitInNumerator(num)
                    if num2 is not None:
                        self._numerator.remove(num2)
                        unit = num*num2
                        if isinstance(unit, (Unit, UnitsFraction)):
                            numList, denList = unit.getUnitsLists()
                            self._numerator += numList
                            self._denominator += denList
                    else:
                        self._numerator.append(num)

            for den in rightDen:
                num = self.unitInNumerator(den)
                if num is not None:
                    self._numerator.remove(num)
                    unit = num/den
                    if isinstance(unit, (Unit, UnitsFraction)):
                        numList, denList = unit.getUnitsLists()
                        self._numerator += numList
                        self._denominator += denList
                else:
                    den2 = self.unitInDenominator(den)
                    if den2 is not None:
                        self._denominator.remove(den2)
                        unit = den*den2
                        if isinstance(unit, (Unit, UnitsFraction)):
                            numList, denList = unit.getUnitsLists()
                            self._numerator += denList
                            self._denominator += numList
                    else:
                        self._denominator.append(den)

        if len(self._numerator) == 0 and len(self._denominator) == 0:
            return 1

        return self

    def __init__(self, left: Union[RepresentableUnit, Iterable, None], right: Union[RepresentableUnit, Iterable, None]=None, *, divide: bool):
        self._numerator: UnitsList_t = self._numerator
        self._denominator: UnitsList_t = self._denominator

    def __hash__(self) -> int:
        return hash(str(self))

    def __str__(self) -> str:
        numList = list(map(str, self._numerator))
        aux = ""
        if len(self._numerator) != 0:
            aux = "*".join(numList)
        else:
            aux = "1"
        if len(self._denominator) != 0:
            aux += "/"
            if len(self._denominator) == 1:
                aux += str(self._denominator[0])
            else:
                denList = list(map(str, self._denominator))
                aux += "(" + "*".join(denList) + ")"
        return aux


    @property
    def numerator(self) -> UnitsList_t:
        return list(self._numerator)

    @property
    def denominator(self) -> UnitsList_t:
        return list(self._denominator)


    def getUnitsLists(self) -> Tuple[UnitsList_t, UnitsList_t]:
        return (list(self._numerator), list(self._denominator))

    def hasSameUnit(self, other) -> bool:
        otherNum, otherDen = other.getUnitsLists()
        return Counter(self._numerator) == Counter(otherNum) and Counter(self._denominator) == Counter(otherDen)


    def __eq__(self, other) -> bool:
        if isinstance(other, Number):
            return False
        otherNum, otherDen = other.getUnitsLists()
        return self._numerator == otherNum and self._denominator == otherDen

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)


    def unitInNumerator(self, unit: Unit) -> Optional[Unit]:
        for num in self._numerator:
            if unit.hasSameBaseUnit(num):
                return num
        return None

    def unitInDenominator(self, unit: Unit) -> Optional[Unit]:
        for den in self._denominator:
            if unit.hasSameBaseUnit(den):
                return den
        return None


    def __mul__(self, other):
        if isinstance(other, (Unit, UnitsFraction)):
            return UnitsFraction(self, other, divide=False)

        return super().__mul__(other)

    def __rmul__(self, other):
        if isinstance(other, (Unit, UnitsFraction)):
            return UnitsFraction(other, self, divide=False)

        return super().__rmul__(other)


    def __truediv__(self, other):
        if isinstance(other, (Unit, UnitsFraction)):
            return UnitsFraction(self, other, divide=True)

        return super().__truediv__(other)

    def __rtruediv__(self, other):
        if isinstance(other, (Unit, UnitsFraction)):
            return UnitsFraction(other, self, divide=True)

        return super().__rtruediv__(other)


    def __pow__(self, other: Number) -> Unit:
        if isinstance(other, Number):
            numerator = list()
            denominator = list()
            for num in self._numerator:
                numerator.append(num**other)
            for den in self._denominator:
                denominator.append(den**other)
            return UnitsFraction(numerator, divide=False) / UnitsFraction(denominator, divide=False)

        return super().__pow__(other)



class RepresentableValueUnit(ABC):
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
    def __str__(self) -> str:
        pass

    def __repr__(self) -> str:
        return self.__str__()


    @property
    @abstractmethod
    def value(self) -> Number:
        pass

    @property
    @abstractmethod
    def unit(self) -> RepresentableUnit:
        pass

    @property
    @abstractmethod
    def exp10(self) -> int:
        pass


    @abstractmethod
    def getUnit(self) -> RepresentableUnit:
        pass

    @abstractmethod
    def getUnitsLists(self) -> Tuple[UnitsList_t, UnitsList_t]:
        pass

    @abstractmethod
    def hasSameUnit(self, other) -> bool:
        pass


    @abstractmethod
    def __neg__(self) -> RepresentableValueUnit:
        pass

    @abstractmethod
    def __pos__(self) -> RepresentableValueUnit:
        pass

    @abstractmethod
    def __abs__(self) -> RepresentableValueUnit:
        pass


    @abstractmethod
    def __int__(self) -> int:
        pass
    @abstractmethod
    def __float__(self) -> float:
        pass
    @abstractmethod
    def __complex__(self) -> complex:
        pass


    @abstractmethod
    def __round__(self, ndigits=0):
        pass
    @abstractmethod
    def __trunc__(self):
        pass
    @abstractmethod
    def __floor__(self):
        pass
    @abstractmethod
    def __ceil__(self):
        pass


    @abstractmethod
    def __eq__(self, other) -> bool:
        pass
    @abstractmethod
    def __ne__(self, other) -> bool:
        pass
    @abstractmethod
    def __lt__(self, other) -> bool:
        pass
    @abstractmethod
    def __le__(self, other) -> bool:
        pass
    @abstractmethod
    def __gt__(self, other) -> bool:
        pass
    @abstractmethod
    def __ge__(self, other) -> bool:
        pass


    @abstractmethod
    def __add__(self, other):
        pass

    @abstractmethod
    def __radd__(self, other):
        pass


    @abstractmethod
    def __sub__(self, other):
        pass

    @abstractmethod
    def __rsub__(self, other):
        pass


    @abstractmethod
    def __mul__(self, other):
        pass

    @abstractmethod
    def __rmul__(self, other):
        pass


    @abstractmethod
    def __truediv__(self, other):
        pass

    @abstractmethod
    def __rtruediv__(self, other):
        pass


    @abstractmethod
    def __pow__(self, other: Number):
        pass


class ValueUnits(RepresentableValueUnit):

    # attributes:
    # self._value: Number
    # self._unit: RepresentableUnit
    # self._exp10: int

    # inmutable

    def __new__(cls, value: Number, unit: RepresentableUnit, exp10: int=0):
        assert(isinstance(value, Number))
        assert(isinstance(unit, RepresentableUnit))
        self = super(ValueUnits, cls).__new__(cls)

        if unit == 1:
            return value*(10**exp10)

        if not isinstance(exp10, int):
            raise TypeError("Parameter `exp10` must be an int, not an " + type(exp10) + ".")

        return self

    def __init__(self, value: Number, unit: RepresentableUnit, exp10: int=0):
        self._value: Number = value
        self._unit: RepresentableUnit = unit
        self._exp10: int = exp10

    def __hash__(self) -> int:
        return hash(str(self))

    def __str__(self) -> str:
        result = str(self._value)
        if self._exp10 != 0:
            result += "e"+str(self._exp10)
        result += " ["+str(self._unit)+"]"
        return result


    @property
    def value(self) -> Number:
        return self._value

    @property
    def unit(self) -> RepresentableUnit:
        return self._unit

    @property
    def exp10(self) -> int:
        return self._exp10


    def getUnit(self) -> RepresentableUnit:
        return self._unit

    def getUnitsLists(self) -> Tuple[UnitsList_t, UnitsList_t]:
        return self._unit.getUnitsLists()

    def hasSameUnit(self, other) -> bool:
        if isinstance(other, RepresentableUnit):
            return self._unit.hasSameUnit(other)
        return self._unit.hasSameUnit(other.getUnit())


    def __neg__(self) -> RepresentableValueUnit:
        return ValueUnits(-self._value, self._unit, self._exp10)
    def __pos__(self) -> RepresentableValueUnit:
        return ValueUnits(self._value, self._unit, self._exp10)
    def __abs__(self) -> RepresentableValueUnit:
        return ValueUnits(abs(self._value), self._unit, self._exp10)


    def __int__(self) -> int:
        return int(self._value*(10**self._exp10))
    def __float__(self) -> float:
        return float(self._value*(10**self._exp10))
    def __complex__(self) -> complex:
        return complex(self._value*(10**self._exp10))


    def __round__(self, ndigits=0):
        return ValueUnits(round(self._value, ndigits), self._unit, self._exp10)
    def __trunc__(self):
        return ValueUnits(trunc(self._value), self._unit, self._exp10)
    def __floor__(self):
        return ValueUnits(floor(self._value), self._unit, self._exp10)
    def __ceil__(self):
        return ValueUnits(ceil(self._value), self._unit, self._exp10)


    def __eq__(self, other) -> bool:
        if isinstance(other, RepresentableValueUnit):
            if self.hasSameUnit(other):
                if self._value*(10**self._exp10) == other.value*(10**other.exp10):
                    return True
        return False
    def __ne__(self, other) -> bool:
        return not self.__eq__(other)
    def __lt__(self, other) -> bool:
        if isinstance(other, RepresentableValueUnit):
            if self.hasSameUnit(other):
                if self.value*(10**self.exp10) < other.value*(10**other.exp10):
                    return True
        return False
    def __le__(self, other) -> bool:
        if isinstance(other, RepresentableValueUnit):
            if self.hasSameUnit(other):
                if self._value*(10**self._exp10) <= other._value*(10**other._exp10):
                    return True
        return False
    def __gt__(self, other) -> bool:
        return not self.__le__(other)
    def __ge__(self, other) -> bool:
        return not self.__lt__(other)


    def __add__(self, other):
        if isinstance(other, RepresentableValueUnit):
            if self.hasSameUnit(other):
                unit = self._unit
                exp10 = self._exp10
                if self._exp10 == other._exp10:
                    value = self._value + other._value
                else:
                    value = self._value + other._value*10**(other._exp10-self._exp10)
                return ValueUnits(value, unit, exp10)
        return NotImplemented

    def __radd__(self, other):
        if isinstance(other, RepresentableValueUnit):
            if self.hasSameUnit(other):
                unit = self._unit
                exp10 = self._exp10
                if self._exp10 == other._exp10:
                    value = self._value + other._value
                else:
                    value = self._value + other._value*10**(other._exp10-self._exp10)
                return ValueUnits(value, unit, exp10)
        return NotImplemented


    def __sub__(self, other):
        if isinstance(other, RepresentableValueUnit):
            if self.hasSameUnit(other):
                unit = self._unit
                exp10 = self._exp10
                if self._exp10 == other._exp10:
                    value = self._value - other._value
                else:
                    value = self._value - other._value*10**(other._exp10-self._exp10)
                return ValueUnits(value, unit, exp10)
        return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, RepresentableValueUnit):
            if self.hasSameUnit(other):
                unit = self._unit
                exp10 = self._exp10
                if self._exp10 == other._exp10:
                    value = other._value - self._value
                else:
                    value = other._value*10**(other._exp10-self._exp10) - self._value
                return ValueUnits(value, unit, exp10)
        return NotImplemented


    def __mul__(self, other):
        if isinstance(other, Number):
            value = self._value * other
            return ValueUnits(value, self._unit, self._exp10)
        if isinstance(other, ValueUnits):
            value = self._value * other._value
            unit = self._unit * other._unit
            exp10 = self._exp10 + other._exp10
            return ValueUnits(value, unit, exp10)
        return NotImplemented

    def __rmul__(self, other):
        if isinstance(other, Number):
            value = self._value * other
            return ValueUnits(value, self._value, self._exp10)
        if isinstance(other, ValueUnits):
            value = self._value * other._value
            unit = self._unit * other._unit
            exp10 = self._exp10 + other._exp10
            return ValueUnits(value, unit, exp10)
        return NotImplemented


    def __truediv__(self, other):
        if isinstance(other, Number):
            value = self._value / other
            return ValueUnits(value, self._value, self._exp10)
        if isinstance(other, ValueUnits):
            value = self._value / other._value
            unit = self._unit / other._unit
            exp10 = self._exp10 - other._exp10
            return ValueUnits(value, unit, exp10)
        return NotImplemented

    def __rtruediv__(self, other):
        if isinstance(other, Number):
            value = other / self._value
            unit = None / self._unit
            exp10 = 0 - self._exp10
            return ValueUnits(value, unit, exp10)
        if isinstance(other, ValueUnits):
            value = other._value / self._value
            unit = other._unit / self._unit
            exp10 = other._exp10 - self._exp10
            return ValueUnits(value, unit, exp10)
        return NotImplemented


    def __pow__(self, other: Number):
        if isinstance(other, Number):
            value = self._value ** other
            unit = self._unit ** other
            exp10 = self._exp10 * other
            return ValueUnits(value, unit, exp10)

        return NotImplemented

