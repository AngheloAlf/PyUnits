from abc import ABC, abstractmethod
from Prefixes import magnitudeFactor, isValidPrefix


class RepresentableUnit(ABC):
    def className(self):
        return self.__class__.__name__

    @abstractmethod
    def baseUnitStr(self):
        pass

    @abstractmethod
    def unitWithPrefixStr(self):
        pass

    @abstractmethod
    def valueStr(self):
        pass

    def __str__(self):
        return f"<{self.valueStr()} {self.unitWithPrefixStr()}>"


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


    @abstractmethod
    def getClass(self):
        pass

    def instanceChild(self, *args, **kwargs):
        return self.getClass()(*args, **kwargs)


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
        return self._value * (10**(self._exp10 + magnitudeFactor(self._prefix, new_pre)))

    def baseUnitStr(self):
        return self._unit

    def unitWithPrefixStr(self):
        return f"{self._prefix}{self._unit}"

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


    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return self.getClass()(self._value * other, prefix=self._prefix, exp10=self._exp10, priority=self._priority)
        return MulUnits(self, other)

    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            return self.getClass()(self._value * other, prefix=self._prefix, exp10=self._exp10, priority=self._priority)
        return MulUnits(other, self)


    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError()
            return self.getClass()(self._value / other, prefix=self._prefix, exp10=self._exp10, priority=self._priority)

        if other.value() == 0:
            raise ZeroDivisionError()

        if isinstance(other, (self.getClass())):
            left = self.value()
            right = other.value()
            return left/right

        return DivUnits(self, other)

    def __rtruediv__(self, other):
        if self.value() == 0:
            raise ZeroDivisionError()

        if isinstance(other, (int, float)):
            return DivUnits(DimensionLessUnit(other), self)

        if isinstance(other, (self.getClass())):
            left = other.value()
            right = self.value()
            return left/right

        return DivUnits(other, self)


class PairUnits(RepresentableUnit):
    def __init__(self, left, right, scalar=1):
        assert(isinstance(left, (BaseUnit, PairUnits)))
        assert(isinstance(right, (BaseUnit, PairUnits)))
        assert(isinstance(scalar, (int, float)))
        self._scalar = scalar
        self._left = left
        self._right = right


    @abstractmethod
    def value(self, *, use_actual_prefix=False):
        pass


    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return MulUnits(self._left, self._right, self._scalar*other)
        return MulUnits(self, other)

    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            return MulUnits(self._left, self._right, self._scalar*other)
        return MulUnits(other, self)


    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError()
            return DivUnits(self._left, self._right, self._scalar*other)

        if other.value() == 0:
            raise ZeroDivisionError()

        return DivUnits(self, other)

    def __rtruediv__(self, other):
        if self.value() == 0:
            raise ZeroDivisionError()

        if isinstance(other, (int, float)):
            return DivUnits(DimensionLessUnit(other), self)
        return DivUnits(other, self)


class MulUnits(PairUnits):
    def value(self, *, use_actual_prefix=False):
        left = self._left.value(use_actual_prefix=use_actual_prefix)
        right = self._right.value(use_actual_prefix=use_actual_prefix)
        return self._scalar * left * right


    def baseUnitStr(self):
        left = self._left.baseUnitStr()
        right = self._right.baseUnitStr()
        return f"{left}*{right}"

    def unitWithPrefixStr(self):
        left = self._left.unitWithPrefixStr()
        right = self._right.unitWithPrefixStr()
        return f"{left}*{right}"

    def valueStr(self):
        if self._scalar == 0:
            return "0"
        left = self._left.valueStr()
        if left == "0":
            return "0"
        right = self._right.valueStr()
        if right == "0":
            return "0"
        scalar = ""
        if self._scalar != 1:
            scalar = f"{self._scalar}*"
        return f"{scalar}{left}*{right}"


class DivUnits(PairUnits):
    def value(self, *, use_actual_prefix=False):
        left = self._left.value(use_actual_prefix=use_actual_prefix)
        right = self._right.value(use_actual_prefix=use_actual_prefix)
        return left / right / self._scalar


    def baseUnitStr(self):
        left = self._left.baseUnitStr()
        right = self._right.baseUnitStr()
        return f"{left}/({right})"

    def unitWithPrefixStr(self):
        left = self._left.unitWithPrefixStr()
        right = self._right.unitWithPrefixStr()
        return f"{left}/({right})"

    def valueStr(self):
        if self._scalar == 0:
            raise ZeroDivisionError()
        left = self._left.valueStr()
        if left == "0":
            return "0"
        right = self._right.valueStr()
        if right == "0":
            raise ZeroDivisionError()
        scalar = ""
        if self._scalar != 1:
            scalar = f"{self._scalar}*"
        return f"{left}/({scalar}{right})"


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




a = LengthUnit(15)
b = MassUnit(8)
c = TimeUnit(2)

# print(a, a.value())
# print(b, b.value())
# print(c, c.value())

n = (a+a)*b/(c*c)/5
n2 = (a+a)*b/c/c/5

# print(n, n.value())
# print(n2, n2.value())

print(a._value)

print(a*b/a)

