from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Tuple
from collections import Counter

from Prefixes import magnitudeFactor, isValidPrefix


class RepresentableUnit(ABC):
    @abstractmethod
    def copy(self):
        pass

    @abstractmethod
    def mulByNumber(self, number):
        pass

    @abstractmethod
    def divByNumber(self, number):
        pass

    def className(self):
        return self.__class__.__name__

    @abstractmethod
    def getClass(self):
        pass

    def instanceChild(self, *args, **kwargs):
        return self.getClass()(*args, **kwargs)

    @abstractmethod
    def baseUnit(self):
        pass

    @abstractmethod
    def baseUnitStr(self):
        pass

    @abstractmethod
    def unitWithPrefix(self):
        pass

    @abstractmethod
    def unitWithPrefixStr(self):
        pass

    @abstractmethod
    def valueStr(self):
        pass

    def __str__(self):
        return f"<{self.valueStr()} [{self.unitWithPrefixStr()}]>"

    def __repr__(self):
        return self.__str__()


    def __mul__(self, other):
        return CombinationUnits(self, other, divide=False)

    def __rmul__(self, other):
        return CombinationUnits(other, self, divide=False)


    def __truediv__(self, other):
        return CombinationUnits(self, other, divide=True)

    def __rtruediv__(self, other):
        return CombinationUnits(other, self, divide=True)



class BaseUnit(RepresentableUnit):
    def __init__(self, value, prefix, exp10, priority, default_prefix, unit):
        assert(isValidPrefix(prefix))
        assert(isValidPrefix(default_prefix))

        self._value = value
        self._prefix = prefix
        self._exp10 = exp10

        self._priority = priority

        self._default_prefix = default_prefix
        self._unit = unit

    def copy(self):
        obj = object.__new__(self.getClass())

        obj._value = self._value
        obj._prefix = self._prefix
        obj._exp10 = self._exp10

        obj._priority = self._priority

        obj._default_prefix = self._default_prefix
        obj._unit = self._unit

        return obj

    def mulByNumber(self, number):
        assert(isinstance(number, (int, float)))
        result = self.copy()
        result._value *= number
        return result

    def divByNumber(self, number):
        assert(isinstance(number, (int, float)))
        if number == 0:
            raise ZeroDivisionError()
        result = self.copy()
        result._value /= number
        return result


    def value(self, *, new_prefix=None, use_actual_prefix=False):
        validate_params = new_prefix==None and use_actual_prefix==False
        validate_params = validate_params or (new_prefix!=None and use_actual_prefix==False)
        validate_params = validate_params or (new_prefix==None and use_actual_prefix==True)
        assert(validate_params)

        new_pre = self._default_prefix
        if new_prefix != None:
            assert(isValidPrefix(new_prefix))
            new_pre = new_prefix
        if use_actual_prefix:
            new_pre = self._prefix

        factor = 10**(self._exp10 + magnitudeFactor(self._prefix, new_pre))
        result = self._value * factor
        return result

    def baseUnit(self):
        return ([self._unit], [])

    def baseUnitStr(self):
        return self.baseUnit()[0][0]

    def unitWithPrefix(self):
        return ([f"{self._prefix}{self._unit}"], [])

    def unitWithPrefixStr(self):
        return self.unitWithPrefix()[0][0]

    def valueStr(self):
        exp = ""
        if self._exp10:
            exp = f"e{self._exp10}"
        return f"{self._value}{exp}"


    def _dataForAddsAndSubs(self, other):
        if not isinstance(other, BaseUnit):
            raise TypeError("no u")

        left = 0
        right = 0
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


    def __add__(self, other):
        if not isinstance(other, self.getClass()):
            return NotImplemented

        left, right, prefix, exp10, priority = self._dataForAddsAndSubs(other)
        return self.instanceChild(left + right, prefix=prefix, exp10=exp10, priority=priority)

    def __radd__(self, other):
        if not isinstance(other, self.getClass()):
            return NotImplemented

        right, left, prefix, exp10, priority = self._dataForAddsAndSubs(other)
        return self.instanceChild(left + right, prefix=prefix, exp10=exp10, priority=priority)


    def __sub__(self, other):
        if not isinstance(other, self.getClass()):
            return NotImplemented

        left, right, prefix, exp10, priority = self._dataForOperator(other)
        return self.instanceChild(left - right, prefix=prefix, exp10=exp10, priority=priority)

    def __rsub__(self, other):
        if not isinstance(other, self.getClass()):
            return NotImplemented

        right, left, prefix, exp10, priority = self._dataForOperator(other)
        return self.instanceChild(left - right, prefix=prefix, exp10=exp10, priority=priority)


class DimensionLessUnit(BaseUnit):
    def __init__(self, value, *, prefix="", exp10=0, priority=None):
        super().__init__(value, prefix=prefix, exp10=exp10, priority=priority, default_prefix="", unit="_")

    def getClass(self):
        return DimensionLessUnit

class LengthUnit(BaseUnit):
    def __init__(self, value, *, prefix="", exp10=0, priority=None):
        super().__init__(value, prefix=prefix, exp10=exp10, priority=priority, default_prefix="", unit="m")

    def getClass(self):
        return LengthUnit

class MassUnit(BaseUnit):
    def __init__(self, value, *, prefix="k", exp10=0, priority=None):
        super().__init__(value, prefix=prefix, exp10=exp10, priority=priority, default_prefix="k", unit="g")

    def getClass(self):
        return MassUnit

class TemperatureUnit(BaseUnit):
    def __init__(self, value, *, prefix="", exp10=0, priority=None):
        super().__init__(value, prefix=prefix, exp10=exp10, priority=priority, default_prefix="", unit="K")

    def getClass(self):
        return TemperatureUnit

class TimeUnit(BaseUnit):
    def __init__(self, value, *, prefix="", exp10=0, priority=None):
        super().__init__(value, prefix=prefix, exp10=exp10, priority=priority, default_prefix="", unit="s")

    def getClass(self):
        return TimeUnit

class SubstanceUnit(BaseUnit):
    def __init__(self, value, *, prefix="", exp10=0, priority=None):
        super().__init__(value, prefix=prefix, exp10=exp10, priority=priority, default_prefix="", unit="mol")

    def getClass(self):
        return SubstanceUnit

class ElectricCurrentUnit(BaseUnit):
    def __init__(self, value, *, prefix="", exp10=0, priority=None):
        super().__init__(value, prefix=prefix, exp10=exp10, priority=priority, default_prefix="", unit="A")

    def getClass(self):
        return ElectricCurrentUnit

class LuminousIntensityUnit(BaseUnit):
    def __init__(self, value, *, prefix="", exp10=0, priority=None):
        super().__init__(value, prefix=prefix, exp10=exp10, priority=priority, default_prefix="", unit="cd")

    def getClass(self):
        return LuminousIntensityUnit


class CombinationUnits(RepresentableUnit):
    def __new__(cls, left, right, *, divide: bool):
        # at most one is a number
        assert(not (isinstance(left, (int, float)) and isinstance(right, (int, float))))

        if isinstance(left, (int, float)):
            if left == 1:
                return CombinationUnits(None, right, divide=divide)

            if divide:
                if right.value() == 0:
                    raise ZeroDivisionError()
                tmp = CombinationUnits(None, right, divide=divide)
                return tmp.mulByNumber(left)
            else:
                return right.mulByNumber(left)
        elif isinstance(right, (int, float)):
            if right == 1:
                return CombinationUnits(left, None, divide=divide)

            if divide:
                if right == 0:
                    raise ZeroDivisionError()
                return left.divByNumber(right)
            else:
                return left.mulByNumber(right)

        if divide and right.value() == 0:
            raise ZeroDivisionError()

        if divide and isinstance(left, BaseUnit) and isinstance(right, left.getClass()):
            result = left.value() / right.value()
            return result


        if isinstance(left, CombinationUnits) and isinstance(right, BaseUnit):
            if divide:
                return left.divByUnit(right)
            else:
                return left.mulByUnit(right)

        if isinstance(left, BaseUnit) and isinstance(right, CombinationUnits):
            if divide:
                tmp = CombinationUnits(None, right, divide=divide)
                return tmp.mulByUnit(left)
            else:
                return right.mulByUnit(left)

        if isinstance(left, CombinationUnits) and isinstance(right, CombinationUnits):
            result = left.copy()
            for unit in right._numerator:
                if divide:
                    result = result.divByUnit(unit)
                else:
                    result = result.mulByUnit(unit)

            for unit in right._denominator:
                if divide:
                    result = result.mulByUnit(unit)
                else:
                    result = result.divByUnit(unit)

            if divide:
                result.divByNumber(right._num_scalar)
                result.mulByNumber(right._denom_scalar)
            else:
                result.mulByNumber(right._num_scalar)
                result.divByNumber(right._denom_scalar)

            return result

        return object.__new__(cls)


    def __init__(self, left, right, *, divide: bool):
        if len(self.__dict__) > 0:
            return
        assert(isinstance(left, (BaseUnit, CombinationUnits, type(None))))
        assert(isinstance(right, (BaseUnit, CombinationUnits, type(None))))
        assert(not (left is None and right is None))

        self._numerator = []
        self._denominator = []
        self._num_scalar = 1
        self._denom_scalar = 1

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

    def copy(self):
        obj = object.__new__(self.getClass())

        obj._num_scalar = self._num_scalar
        obj._denom_scalar = self._denom_scalar

        obj._numerator = list(self._numerator)
        obj._denominator = list(self._denominator)

        return obj

    def mulByNumber(self, number):
        assert(isinstance(number, (int, float)))
        result = self.copy()
        result._num_scalar *= number
        return result

    def divByNumber(self, number):
        assert(isinstance(number, (int, float)))
        if number == 0:
            raise ZeroDivisionError()
        result = self.copy()
        result._denom_scalar *= number
        return result


    def unitFromNumerator(self, basic_unit: str) -> Tuple[CombinationUnits, BaseUnit]:
        copy = self.copy()
        for i in range(len(copy._numerator)):
            val = copy._numerator[i]
            if val.baseUnit() == basic_unit:
                del copy._numerator[i]
                return (copy, val)
        return (copy, None)

    def unitFromDenominator(self, basic_unit: str) -> Tuple[CombinationUnits, BaseUnit]:
        copy = self.copy()
        for i in range(len(copy._denominator)):
            val = copy._denominator[i]
            if val.baseUnit() == basic_unit:
                del copy._denominator[i]
                return (copy, val)
        return (copy, None)


    def mulByUnit(self, unit: BaseUnit) -> CombinationUnits:
        assert(isinstance(unit, BaseUnit))
        result, val = self.unitFromDenominator(unit.baseUnit())
        if val != None:
            aux = unit/val
            return result.mulByNumber(aux)
        result._numerator.append(unit)
        return result


    def divByUnit(self, unit: BaseUnit) -> CombinationUnits:
        assert(isinstance(unit, BaseUnit))
        result, val = self.unitFromNumerator(unit.baseUnit())
        if val != None:
            aux = val/unit
            return result.mulByNumber(aux)
        result._denominator.append(unit)
        return result


    # TODO: this
    def __add__(self, other):
        if not isinstance(other, self.getClass()):
            return NotImplemented

        num1, denom1 = self.baseUnit()
        num2, denom2 = other.baseUnit()
        if not (Counter(num1) == Counter(num2) and Counter(denom1) == Counter(denom2)):
            raise TypeError(f"unsupported operand units for +: '{self.baseUnitStr()}' and '{other.baseUnitStr()}'")

        return NotImplemented

    # TODO: this
    def __radd__(self, other):
        if not isinstance(other, self.getClass()):
            return NotImplemented

        num1, denom1 = self.baseUnit()
        num2, denom2 = other.baseUnit()
        if not (Counter(num1) == Counter(num2) and Counter(denom1) == Counter(denom2)):
            raise TypeError(f"unsupported operand units for +: '{other.baseUnitStr()}' and '{self.baseUnitStr()}'")

        return NotImplemented


    # TODO: this
    def __sub__(self, other):
        if not isinstance(other, self.getClass()):
            return NotImplemented

        num1, denom1 = self.baseUnit()
        num2, denom2 = other.baseUnit()
        if not (Counter(num1) == Counter(num2) and Counter(denom1) == Counter(denom2)):
            raise TypeError(f"unsupported operand units for -: '{self.baseUnitStr()}' and '{other.baseUnitStr()}'")

        return NotImplemented

    # TODO: this
    def __rsub__(self, other):
        if not isinstance(other, self.getClass()):
            return NotImplemented

        num1, denom1 = self.baseUnit()
        num2, denom2 = other.baseUnit()
        if not (Counter(num1) == Counter(num2) and Counter(denom1) == Counter(denom2)):
            raise TypeError(f"unsupported operand units for -: '{other.baseUnitStr()}' and '{self.baseUnitStr()}'")

        return NotImplemented


    def getClass(self):
        return CombinationUnits

    def baseUnit(self):
        num_units = []
        denom_units = []

        for i in self._numerator:
            num, den = i.baseUnit()
            num_units += num
            denom_units += den

        for i in self._denominator:
            num, den = i.baseUnit()
            denom_units += num
            num_units += den
        
        return (num_units, denom_units)

    def baseUnitStr(self):
        num_units, denom_units = self.baseUnit()

        num_unit = "1"
        if len(num_units) > 0:
            num_unit = "*".join(num_units)

        denom_unit = ""
        if len(denom_units) > 0:
            denom_unit = "*".join(denom_units)
            denom_unit = f"/({denom_unit})"

        return f"{num_unit}{denom_unit}"

    def unitWithPrefix(self):
        num_units = []
        denom_units = []

        for i in self._numerator:
            num, den = i.unitWithPrefix()
            num_units += num
            denom_units += den

        for i in self._denominator:
            num, den = i.unitWithPrefix()
            denom_units += num
            num_units += den

        return (num_units, denom_units)

    def unitWithPrefixStr(self):
        num_units, denom_units = self.unitWithPrefix()

        num_unit = "1"
        if len(num_units) > 0:
            num_unit = "*".join(num_units)

        denom_unit = ""
        if len(denom_units) > 0:
            denom_unit = "*".join(denom_units)
            denom_unit = f"/({denom_unit})"

        return f"{num_unit}{denom_unit}"

    def valueStr(self):
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


    def value(self, *, use_actual_prefix=False):
        num_result = self._num_scalar
        for i in self._numerator:
            num_result *= i.value(use_actual_prefix=use_actual_prefix)

        denom_result = self._denom_scalar
        for i in self._denominator:
            denom_result *= i.value(use_actual_prefix=use_actual_prefix)

        return num_result/denom_result


a = LengthUnit(15)
b = MassUnit(8)
c = TimeUnit(2)

n = a*b/(c*c)

print(n, n.value())

test = n + a*b
print(test, test.value())
