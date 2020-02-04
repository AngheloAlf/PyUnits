from __future__ import annotations

from abc import ABC, abstractmethod
from collections import Counter
from typing import Union, Optional, List, Tuple
NumberType = Union[int, float]

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

    @abstractmethod
    def getClass(self):
        pass

    def instanceChild(self, *args, **kwargs):
        return self.getClass()(*args, **kwargs)

    def className(self) -> str:
        return self.__class__.__name__


    @abstractmethod
    def unitWithoutPrefix(self) -> Tuple[List[str], List[str]]:
        pass

    @abstractmethod
    def unitWithPrefix(self) -> Tuple[List[str], List[str]]:
        pass

    def _parseUnitsToStr(self, num_units: List[str], denom_units: List[str]) -> str:
        if len(num_units) == 0 and len(denom_units) == 0:
            return ""

        num_unit = "1"
        if len(num_units) > 0:
            num_unit = "*".join(num_units)

        denom_unit = ""
        if len(denom_units) > 0:
            denom_unit = "*".join(denom_units)
            denom_unit = f"/({denom_unit})"

        return f"{num_unit}{denom_unit}"

    def unitWithoutPrefixStr(self) -> str:
        num_units, denom_units = self.unitWithoutPrefix()
        return self._parseUnitsToStr(num_units, denom_units)

    def unitWithPrefixStr(self) -> str:
        num_units, denom_units = self.unitWithPrefix()
        return self._parseUnitsToStr(num_units, denom_units)

    @abstractmethod
    def valueStr(self) -> str:
        pass


    # @abstractmethod
    # def value(self, *, ) -> Number:
    #     pass


    def __str__(self) -> str:
        return f"<{self.valueStr()} [{self.unitWithPrefixStr()}]>"

    def __repr__(self) -> str:
        return self.__str__()


    @abstractmethod
    def mulByNumber(self, number: NumberType):
        pass

    @abstractmethod
    def divByNumber(self, number: NumberType):
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


    def __mul__(self, other):
        return CombinationUnits(self, other, divide=False)

    def __rmul__(self, other):
        return CombinationUnits(other, self, divide=False)


    def __truediv__(self, other):
        return CombinationUnits(self, other, divide=True)

    def __rtruediv__(self, other):
        return CombinationUnits(other, self, divide=True)


class BaseUnit(RepresentableUnit):
    def __init__(self, value: NumberType, prefix: str, exp10: int, priority: Optional[bool], default_prefix: str, unit: str):
        assert(SIPrefixes.isValidPrefix(prefix))
        assert(SIPrefixes.isValidPrefix(default_prefix))

        self._value = value
        self._prefix = prefix
        self._exp10 = exp10

        self._priority = priority

        self._default_prefix = default_prefix
        self._unit = unit


    def unitWithoutPrefix(self) -> Tuple[List[str], List[str]]:
        return ([self._unit], [])

    def unitWithPrefix(self) -> Tuple[List[str], List[str]]:
        return ([f"{self._prefix}{self._unit}"], [])

    def valueStr(self) -> str:
        exp = ""
        if self._exp10:
            exp = f"e{self._exp10}"
        return f"{self._value}{exp}"


    def value(self, *, new_prefix=None, use_actual_prefix=False) -> NumberType:
        validate_params = new_prefix==None and use_actual_prefix==False
        validate_params = validate_params or (new_prefix!=None and use_actual_prefix==False)
        validate_params = validate_params or (new_prefix==None and use_actual_prefix==True)
        assert(validate_params)

        new_pre = self._default_prefix
        if new_prefix != None:
            assert(SIPrefixes.isValidPrefix(new_prefix))
            new_pre = new_prefix
        if use_actual_prefix:
            new_pre = self._prefix

        factor = 10**(self._exp10 + SIPrefixes.magnitudeFactor(self._prefix, new_pre))
        result = self._value * factor
        return result


    def mulByNumber(self, number: NumberType) -> BaseUnit:
        assert(isinstance(number, (int, float)))
        result = self.copy()
        result._value *= number
        return result

    def divByNumber(self, number: NumberType) -> BaseUnit:
        assert(isinstance(number, (int, float)))
        if number == 0:
            raise ZeroDivisionError()
        result = self.copy()
        result._value /= number
        return result


    def _dataForAddsAndSubs(self, other: BaseUnit) -> Tuple[NumberType, NumberType, str, int, bool]:
        if not isinstance(other, BaseUnit):
            raise TypeError("no u")

        prefix = ""
        exp10 = 0
        priority = None

        if(self._priority):
            prefix = self._prefix
            priority = True
        elif(other._priority):
            prefix = other._prefix
            priority = True
        else:
            prefix = self._default_prefix
            priority = False

        left = self.value(new_prefix=prefix)
        right = other.value(new_prefix=prefix)

        return (left, right, prefix, exp10, priority)


    def __add__(self, other: BaseUnit) -> BaseUnit:
        if not isinstance(other, self.getClass()):
            return NotImplemented

        left, right, prefix, exp10, priority = self._dataForAddsAndSubs(other)
        return self.instanceChild(left + right, prefix=prefix, exp10=exp10, priority=priority)

    def __radd__(self, other: BaseUnit) -> BaseUnit:
        if not isinstance(other, self.getClass()):
            return NotImplemented

        right, left, prefix, exp10, priority = self._dataForAddsAndSubs(other)
        return self.instanceChild(left + right, prefix=prefix, exp10=exp10, priority=priority)


    def __sub__(self, other: BaseUnit) -> BaseUnit:
        if not isinstance(other, self.getClass()):
            return NotImplemented

        left, right, prefix, exp10, priority = self._dataForAddsAndSubs(other)
        return self.instanceChild(left - right, prefix=prefix, exp10=exp10, priority=priority)

    def __rsub__(self, other: BaseUnit) -> BaseUnit:
        if not isinstance(other, self.getClass()):
            return NotImplemented

        right, left, prefix, exp10, priority = self._dataForAddsAndSubs(other)
        return self.instanceChild(left - right, prefix=prefix, exp10=exp10, priority=priority)


class CombinationUnits(RepresentableUnit):
    def __new__(cls, left, right, *, divide: bool):
        # at most one is a number or None
        if isinstance(left, (int, float, type(None))) and isinstance(right, (int, float, type(None))):
            raise TypeError("At least one parameter must be an unit or a combination of units.")

        if right is None:
            return left.copy()

        if divide and left is not None:
            if isinstance(right, (int, float)):
                return left.divByNumber(right)

            if isinstance(left, BaseUnit) and isinstance(right, left.getClass()):
                result = left.value() / right.value()
                return result

            new_right = CombinationUnits(None, right, divide=True)
            if left is None:
                return new_right
            return CombinationUnits(left, new_right, divide=False)

        if isinstance(left, (int, float)):
            return right.mulByNumber(left)
        elif isinstance(right, (int, float)):
            return left.mulByNumber(right)

        if isinstance(left, CombinationUnits) and isinstance(right, BaseUnit):
            return left.mulByUnit(right)
        elif isinstance(left, BaseUnit) and isinstance(right, CombinationUnits):
            return right.mulByUnit(left)
        elif isinstance(left, CombinationUnits) and isinstance(right, CombinationUnits):
            result = left.copy()
            for unit in right._numerator:
                result = result.mulByUnit(unit)

            for unit in right._denominator:
                result = result.divByUnit(unit)

            result.mulByNumber(right._num_scalar)
            result.divByNumber(right._denom_scalar)

            num_units, denom_units = result.unitWithoutPrefix()
            if len(num_units) == 0 and len(denom_units) == 0:
                return result.value()

            return result

        return super().__new__(cls)


    def __init__(self, left, right, *, divide: bool):
        if len(self.__dict__) > 0:
            return
        assert(isinstance(left, (BaseUnit, CombinationUnits, type(None))))
        assert(isinstance(right, (BaseUnit, CombinationUnits, type(None))))
        assert(not (left is None and right is None))

        self._numerator: List[BaseUnit] = []
        self._denominator: List[BaseUnit] = []
        self._num_scalar: NumberType = 1
        self._denom_scalar: NumberType = 1

        if left == None:
            pass
        elif isinstance(left, BaseUnit):
            self._numerator.append(left)
        elif isinstance(left, CombinationUnits):
            self._numerator += list(left._numerator)
            self._denominator += list(left._denominator)
            self._num_scalar *= left._num_scalar
            self._denom_scalar *= left._denom_scalar

        if right == None:
            pass
        elif isinstance(right, BaseUnit):
            if divide:
                self._denominator.append(right)
            else:
                self._numerator.append(right)
        elif isinstance(right, CombinationUnits):
            if divide:
                if right.value() == 0:
                    raise ZeroDivisionError()
                self._numerator += list(right._denominator)
                self._denominator += list(right._numerator)
                self._num_scalar *= right._denom_scalar
                self._denom_scalar *= right._num_scalar
            else:
                self._numerator += list(right._numerator)
                self._denominator += list(right._denominator)
                self._num_scalar *= right._num_scalar
                self._denom_scalar *= right._denom_scalar
        return

    def factorizeValuesIntoScalars(self):
        cpy = self.copy()

        for i in range(len(cpy._numerator)):
            value_with_unit = cpy._numerator[i]
            value = value_with_unit.value(use_actual_prefix=True)
            cpy._num_scalar *= value
            cpy._numerator[i] = value_with_unit/value

        for i in range(len(cpy._denominator)):
            value_with_unit = cpy._denominator[i]
            value = value_with_unit.value(use_actual_prefix=True)
            cpy._denom_scalar *= value
            cpy._denominator[i] = value_with_unit/value

        return cpy


    def getClass(self):
        return CombinationUnits


    def unitWithoutPrefix(self) -> Tuple[List[str], List[str]]:
        num_units: List[str] = []
        denom_units: List[str] = []

        for i in self._numerator:
            num, den = i.unitWithoutPrefix()
            num_units += num
            denom_units += den

        for i in self._denominator:
            num, den = i.unitWithoutPrefix()
            denom_units += num
            num_units += den
        
        return (num_units, denom_units)

    def unitWithPrefix(self) -> Tuple[List[str], List[str]]:
        num_units: List[str] = []
        denom_units: List[str] = []

        for i in self._numerator:
            num, den = i.unitWithPrefix()
            num_units += num
            denom_units += den

        for i in self._denominator:
            num, den = i.unitWithPrefix()
            denom_units += num
            num_units += den

        return (num_units, denom_units)

    def valueStr(self) -> str:
        num_units = []
        for i in self._numerator:
            num_units.append(i.valueStr())

        denom_units = []
        for i in self._denominator:
            denom_units.append(i.valueStr())

        num_unit = "1"
        if len(num_units) > 0:
            num_unit = "*".join(num_units)

        denom_unit = ""
        if len(denom_units) > 0:
            denom_unit = "*".join(denom_units)
            denom_unit = f"/({denom_unit})"

        num_scalar = self._num_scalar
        denom_scalar = self._denom_scalar
        
        scalar = ""
        if denom_scalar != 1:
            scalar = f"({num_scalar}/{denom_scalar}) * "
        elif num_scalar != 1:
            scalar = f"{num_scalar} * "

        return f"{scalar}{num_unit}{denom_unit}"


    def numeratorValueWithoutScalar(self, *, use_actual_prefix=False) -> NumberType:
        num_result = 1.0
        for i in self._numerator:
            num_result *= i.value(use_actual_prefix=use_actual_prefix)
        return num_result

    def denominatorValueWithoutScalar(self, *, use_actual_prefix=False) -> NumberType:
        result = 1.0
        for i in self._denominator:
            result *= i.value(use_actual_prefix=use_actual_prefix)
        return result


    def value(self, *, use_actual_prefix=False) -> NumberType:
        num_result = self._num_scalar
        num_result *= self.numeratorValueWithoutScalar(use_actual_prefix=use_actual_prefix)

        denom_result = self._denom_scalar
        denom_result *= self.denominatorValueWithoutScalar(use_actual_prefix=use_actual_prefix)

        return num_result/denom_result


    def unitFromNumerator(self, basic_unit: str) -> Tuple[CombinationUnits, Optional[BaseUnit]]:
        copy = self.copy()
        for i in range(len(copy._numerator)):
            val = copy._numerator[i]
            if val.unitWithoutPrefix()[0][0] == basic_unit:
                del copy._numerator[i]
                return (copy, val)
        return (copy, None)

    def unitFromDenominator(self, basic_unit: str) -> Tuple[CombinationUnits, Optional[BaseUnit]]:
        copy = self.copy()
        for i in range(len(copy._denominator)):
            val = copy._denominator[i]
            if val.unitWithoutPrefix()[0][0] == basic_unit:
                del copy._denominator[i]
                return (copy, val)
        return (copy, None)


    def mulByNumber(self, number: NumberType) -> CombinationUnits:
        assert(isinstance(number, (int, float)))
        result = self.copy()
        result._num_scalar *= number
        return result

    def divByNumber(self, number: NumberType) -> CombinationUnits:
        assert(isinstance(number, (int, float)))
        if number == 0:
            raise ZeroDivisionError()
        result = self.copy()
        result._denom_scalar *= number
        return result


    def mulByUnit(self, unit: BaseUnit) -> CombinationUnits:
        assert(isinstance(unit, BaseUnit))
        result, val = self.unitFromDenominator(unit.unitWithoutPrefix()[0][0])
        if val != None:
            aux = unit/val
            return result.mulByNumber(aux)
        result._numerator.append(unit)
        return result

    def divByUnit(self, unit: BaseUnit) -> CombinationUnits:
        assert(isinstance(unit, BaseUnit))
        result, val = self.unitFromNumerator(unit.unitWithoutPrefix()[0][0])
        if val != None:
            aux = val/unit
            return result.mulByNumber(aux)
        result._denominator.append(unit)
        return result


    def _dataForAddsAndSubs(self, right: CombinationUnits, sign: str) -> Tuple[CombinationUnits, CombinationUnits]:
        num1, denom1 = self.unitWithoutPrefix()
        num2, denom2 = right.unitWithoutPrefix()
        if not (Counter(num1) == Counter(num2) and Counter(denom1) == Counter(denom2)):
            raise TypeError(f"unsupported operand units for {sign}: '{self.unitWithoutPrefixStr()}' and '{right.unitWithoutPrefixStr()}'")

        left = self.factorizeValuesIntoScalars()
        right = right.factorizeValuesIntoScalars()
        return (left, right)


    def __add__(self, other: CombinationUnits) -> CombinationUnits:
        if not isinstance(other, self.getClass()):
            return NotImplemented

        left, right = self._dataForAddsAndSubs(other, "+")

        result = left.copy()
        result._num_scalar = left._num_scalar * right._denom_scalar + right._num_scalar * left._denom_scalar
        result._denom_scalar = left._denom_scalar * right._denom_scalar

        return result

    def __radd__(self, other: CombinationUnits) -> CombinationUnits:
        if not isinstance(other, self.getClass()):
            return NotImplemented

        left, right = other._dataForAddsAndSubs(self, "+")

        result = left.copy()
        result._num_scalar = left._num_scalar * right._denom_scalar + right._num_scalar * left._denom_scalar
        result._denom_scalar = left._denom_scalar * right._denom_scalar

        return result


    def __sub__(self, other: CombinationUnits) -> CombinationUnits:
        if not isinstance(other, self.getClass()):
            return NotImplemented

        left, right = self._dataForAddsAndSubs(other, "-")

        result = left.copy()
        result._num_scalar = left._num_scalar * right._denom_scalar - right._num_scalar * left._denom_scalar
        result._denom_scalar = left._denom_scalar * right._denom_scalar

        return result

    def __rsub__(self, other: CombinationUnits) -> CombinationUnits:
        if not isinstance(other, self.getClass()):
            return NotImplemented

        left, right = other._dataForAddsAndSubs(self, "-")

        result = left.copy()
        result._num_scalar = left._num_scalar * right._denom_scalar - right._num_scalar * left._denom_scalar
        result._denom_scalar = left._denom_scalar * right._denom_scalar

        return result
