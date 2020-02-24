from __future__ import annotations

from abc import ABC, abstractmethod
from numbers import Number, Complex
from math import trunc, floor, ceil
from collections import Counter, Iterable
from typing import List, Tuple, Optional, Union

from ..TypesHelper import Number_t
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
        if isinstance(other, RepresentableUnit):
            return UnitsFraction(self, other, divide=False)
        if isinstance(other, Number):
            return ValueUnits(other, self)
        if other is None:
            return self
        return NotImplemented

    @abstractmethod
    def __rmul__(self, other):
        if isinstance(other, RepresentableUnit):
            return UnitsFraction(other, self, divide=False)
        if isinstance(other, Number):
            return ValueUnits(other, self)
        if other is None:
            return self
        return NotImplemented


    @abstractmethod
    def __truediv__(self, other):
        if isinstance(other, RepresentableUnit):
            return UnitsFraction(self, other, divide=True)
        if isinstance(other, Number):
            return ValueUnits(1/other, self)
        if other is None:
            return self
        return NotImplemented

    @abstractmethod
    def __rtruediv__(self, other):
        if isinstance(other, RepresentableUnit):
            return UnitsFraction(other, self, divide=True)
        if isinstance(other, Number):
            return ValueUnits(other, UnitsFraction(None, self, divide=True))
        if other is None:
            return UnitsFraction(None, self, divide=True)
        return NotImplemented


    @abstractmethod
    def __pow__(self, other: Number_t):
        return NotImplemented


class Unit(RepresentableUnit):

    # attributes:
    # self._unit: str
    # self._defaultPrefix: str
    # self._power: Number_t

    # inmutable

    def __new__(cls, unit: str, defaultPrefix: str="", *, power: Number_t=1):
        self = super(Unit, cls).__new__(cls)

        if not isinstance(unit, str):
            raise TypeError(f"Expected type str for 'unit', not {type(unit).__name__}.")
        if not isinstance(defaultPrefix, str):
            raise TypeError(f"Expected type str for 'defaultPrefix', not {type(defaultPrefix).__name__}.")
        if not SIPrefixes.isValidPrefix(defaultPrefix):
            raise TypeError(f"Invalid prefix: {defaultPrefix}.")
        if not isinstance(power, Number):
            raise TypeError(f"Expected a numeral type for power, not {type(power).__name__}.")

        if power == 0:
            return 1
        elif not isinstance(power, Complex) and power < 0:
            return UnitsFraction(None, Unit(unit, defaultPrefix, power=-power), divide=True)

        return self

    def __init__(self, unit: str, defaultPrefix: str="", *, power: Number_t=1):
        self._unit: str = unit
        self._defaultPrefix: str = defaultPrefix
        self._power: Number_t = power

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
    def power(self) -> Number_t:
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

        return super().__mul__(other)

    def __rmul__(self, other):
        if isinstance(other, Unit) and self.hasSameBaseUnit(other):
            return Unit(self._unit, self._defaultPrefix, power=other._power+self._power)

        return super().__rmul__(other)


    def __truediv__(self, other):
        if isinstance(other, Unit) and self.hasSameBaseUnit(other):
            return Unit(self._unit, self._defaultPrefix, power=self._power-other._power)

        return super().__truediv__(other)

    def __rtruediv__(self, other):
        if isinstance(other, Unit) and self.hasSameBaseUnit(other):
            return Unit(self._unit, self._defaultPrefix, power=other._power-self._power)

        return super().__rtruediv__(other)


    def __pow__(self, other: Number_t) -> Unit:
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

    def __new__(cls, left: Union[RepresentableUnit, Iterable, None], right: Optional[RepresentableUnit]=None, *, divide: bool):
        self = super(UnitsFraction, cls).__new__(cls)

        if not isinstance(left, (RepresentableUnit, Iterable, type(None))):
            raise TypeError("Unexpected type: " + type(left).__name__)
        if not isinstance(right, (RepresentableUnit, type(None))):
            raise TypeError("Unexpected type: " + type(right).__name__)
        if not isinstance(divide, bool):
            raise TypeError("Unexpected type: " + type(divide).__name__)

        self._numerator = list()
        self._denominator = list()

        if isinstance(left, Iterable):
            self._numerator = list(left)
        elif left is not None:
            leftNum, leftDen = left.getUnitsLists()
            self._numerator = list(leftNum)
            self._denominator = list(leftDen)

        if right is not None:
            rightNum, rightDen = right.getUnitsLists()
            if divide:
                rightNum, rightDen = rightDen, rightNum

            for num in rightNum:
                den = self.unitInDenominator(num)
                if den is not None:
                    self._denominator.remove(den)
                    unit = num/den
                    if isinstance(unit, RepresentableUnit):
                        numList, denList = unit.getUnitsLists()
                        self._numerator += numList
                        self._denominator += denList

                else:
                    num2 = self.unitInNumerator(num)
                    if num2 is not None:
                        self._numerator.remove(num2)
                        unit = num*num2
                        if isinstance(unit, RepresentableUnit):
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
                    if isinstance(unit, RepresentableUnit):
                        numList, denList = unit.getUnitsLists()
                        self._numerator += numList
                        self._denominator += denList
                else:
                    den2 = self.unitInDenominator(den)
                    if den2 is not None:
                        self._denominator.remove(den2)
                        unit = den*den2
                        if isinstance(unit, RepresentableUnit):
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
        return super().__mul__(other)

    def __rmul__(self, other):
        return super().__rmul__(other)


    def __truediv__(self, other):
        return super().__truediv__(other)

    def __rtruediv__(self, other):
        return super().__rtruediv__(other)


    def __pow__(self, other: Number_t) -> Unit:
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
    def value(self) -> Number_t:
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
        return False
    @abstractmethod
    def __ne__(self, other) -> bool:
        return False
    @abstractmethod
    def __lt__(self, other) -> bool:
        return False
    @abstractmethod
    def __le__(self, other) -> bool:
        return False
    @abstractmethod
    def __gt__(self, other) -> bool:
        return False
    @abstractmethod
    def __ge__(self, other) -> bool:
        return False


    @abstractmethod
    def __add__(self, other):
        return NotImplemented

    @abstractmethod
    def __radd__(self, other):
        return NotImplemented


    @abstractmethod
    def __sub__(self, other):
        return NotImplemented

    @abstractmethod
    def __rsub__(self, other):
        return NotImplemented


    @abstractmethod
    def __mul__(self, other):
        if isinstance(other, Number):
            value = self.value * other
            return ValueUnits(value, self.unit, self.exp10)
        return NotImplemented

    @abstractmethod
    def __rmul__(self, other):
        if isinstance(other, Number):
            value = other * self.value
            return ValueUnits(value, self.unit, self.exp10)
        return NotImplemented


    @abstractmethod
    def __truediv__(self, other):
        if isinstance(other, Number):
            value = self.value / other
            return ValueUnits(value, self.unit, self.exp10)
        return NotImplemented

    @abstractmethod
    def __rtruediv__(self, other):
        if isinstance(other, Number):
            value = other / self.value
            unit = None / self.unit
            exp10 = 0 - self.exp10
            return ValueUnits(value, unit, exp10)
        return NotImplemented


    @abstractmethod
    def __pow__(self, other: Number_t):
        return NotImplemented


class ValueUnits(RepresentableValueUnit):

    # attributes:
    # self._value: Number_t
    # self._unit: RepresentableUnit
    # self._exp10: int

    # inmutable

    def __new__(cls, value: Number_t, unit: RepresentableUnit, exp10: int=0):
        self = super(ValueUnits, cls).__new__(cls)

        if not isinstance(value, Number):
            raise TypeError("Parameter `value` must be a Number, not an " + type(value).__name__ + ".")
        if not isinstance(unit, RepresentableUnit):
            raise TypeError("Parameter `unit` must be an unit type, not an " + type(unit).__name__ + ".")
        if not isinstance(exp10, int):
            raise TypeError("Parameter `exp10` must be an int, not an " + type(exp10).__name__ + ".")

        if unit == 1:
            return value*(10**exp10)

        return self

    def __init__(self, value: Number_t, unit: RepresentableUnit, exp10: int=0):
        self._value: Number_t = value
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
    def value(self) -> Number_t:
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
                if self.value*(10**self.exp10) <= other.value*(10**other.exp10):
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
        return super().__add__(other)

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
        return super().__radd__(other)


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
        return super().__sub__(other)

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
        return super().__rsub__(other)


    def __mul__(self, other):
        if isinstance(other, RepresentableValueUnit):
            value = self._value * other._value
            unit = self._unit * other._unit
            exp10 = self._exp10 + other._exp10
            return ValueUnits(value, unit, exp10)
        return super().__mul__(other)

    def __rmul__(self, other):
        if isinstance(other, RepresentableValueUnit):
            value = self._value * other._value
            unit = self._unit * other._unit
            exp10 = self._exp10 + other._exp10
            return ValueUnits(value, unit, exp10)
        return super().__rmul__(other)


    def __truediv__(self, other):
        if isinstance(other, RepresentableValueUnit):
            value = self._value / other._value
            unit = self._unit / other._unit
            exp10 = self._exp10 - other._exp10
            return ValueUnits(value, unit, exp10)
        return super().__truediv__(other)

    def __rtruediv__(self, other):
        if isinstance(other, RepresentableValueUnit):
            value = other._value / self._value
            unit = other._unit / self._unit
            exp10 = other._exp10 - self._exp10
            return ValueUnits(value, unit, exp10)
        return super().__rtruediv__(other)


    def __pow__(self, other: Number_t):
        if isinstance(other, Number):
            value = self._value ** other
            unit = self._unit ** other
            exp10 = self._exp10 * other
            return ValueUnits(value, unit, exp10)
        return super().__pow__(other)
