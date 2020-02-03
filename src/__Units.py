from abc import ABC, abstractmethod
from Prefixes import magnitudeFactor, isValidPrefix

class UnitCmInches:
    # def round_nearest(self, decimals=0):
    #     self._value = round_nearest(self._value, decimals)
    #     return

    def __repr__(self):
        name = self.__class__.__name__
        if self._priority != None:
            return f"{name}({self._value}, in_cm={self._in_cm}, priority={self._priority})"
        return f"{name}({self._value}, in_cm={self._in_cm})"



class BaseUnit(ABC):
    def __init__(self, value, prefix, exp10, priority, default_prefix, unit):
        assert(isValidPrefix(prefix))
        assert(isValidPrefix(default_prefix))

        self._value = value
        self._prefix = prefix
        self._exp10 = exp10

        self._priority = priority

        self._default_prefix = default_prefix
        self._unit = unit

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


    def __str__(self):
        return f"<{self.valueStr()} {self.unitWithPrefixStr()}>"


    def _dataForOperator(self, other):
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
        return NotImplemented

    def __sub__(self, other):
        return NotImplemented

    @abstractmethod
    def _multByNumber(self, other):
        pass

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return self._multByNumber(other)
        return MulUnits(self, other)

    # @abstractmethod
    def _divByNumber(self, other):
        pass

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return self._divByNumber(other)
        if self.baseUnitStr() == other.baseUnitStr():
            left = self.value()
            right = other.value()
            return left/right
        return DivUnits(self, other)


class PairUnits(ABC):
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
            return DivUnits(self._left, self._right, self._scalar*other)
        return DivUnits(self, other)

    def __rtruediv__(self, other):
        if isinstance(other, (int, float)):
            return DivUnits(DimensionLessUnit(other), self)
            # return DivUnits(self._left, self._right, self._scalar*other)
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
        right = self._right.valueStr()
        scalar = ""
        if self._scalar != 1:
            scalar = f"{self._scalar}*"
        return f"{scalar}{left}*{right}"

    """
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return MulUnits(self._left, self._right, self._scalar*other)
        return MulUnits(self, other)

    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            return MulUnits(self._left, self._right, self._scalar*other)
        return MulUnits(other, self)
    """

class DivUnits(PairUnits):
    def value(self, *, use_actual_prefix=False):
        left = self._left.value(use_actual_prefix=use_actual_prefix)
        right = self._right.value(use_actual_prefix=use_actual_prefix)
        return left / right / self._scalar


    def baseUnitStr(self):
        left = self._left.baseUnitStr()
        right = self._right.baseUnitStr()
        return f"({left}/{right})"

    def unitWithPrefixStr(self):
        left = self._left.unitWithPrefixStr()
        right = self._right.unitWithPrefixStr()
        return f"({left}/{right})"

    def valueStr(self):
        # if self._scalar == 0:
        #     return 
        left = self._left.valueStr()
        right = self._right.valueStr()
        scalar = ""
        if self._scalar != 1:
            scalar = f"/{self._scalar}"
        return f"({left}/{right}{scalar})"


class DimensionLessUnit(BaseUnit):
    def __init__(self, value, *, prefix="", exp10=0, priority=None):
        super().__init__(value, prefix=prefix, exp10=exp10, priority=priority, default_prefix="", unit="_")

    def getClass(self):
        return DimensionLessUnit


class LengthUnit(BaseUnit):
    def __init__(self, value, *, prefix="", exp10=0, priority=None):
        super().__init__(value, prefix=prefix, exp10=exp10, priority=priority, default_prefix="", unit="m")

    def __add__(self, other):
        if not isinstance(other, LengthUnit):
            return super().__add__(other)

        left, right, prefix, exp10, priority = self._dataForOperator(other)
        return LengthUnit(left + right, prefix=prefix, exp10=exp10, priority=priority)

    def __sub__(self, other):
        if not isinstance(other, LengthUnit):
            return super().__sub__(other)

        left, right, prefix, exp10, priority = self._dataForOperator(other)
        return LengthUnit(left - right, prefix=prefix, exp10=exp10, priority=priority)

    def _multByNumber(self, other):
        return LengthUnit(self._value * other, prefix=self._prefix, exp10=self._exp10, priority=self._priority)


class MassUnit(BaseUnit):
    def __init__(self, value, *, prefix="k", exp10=0, priority=None):
        super().__init__(value, prefix=prefix, exp10=exp10, priority=priority, default_prefix="k", unit="g")

    def __add__(self, other):
        if not isinstance(other, MassUnit):
            return super().__add__(other)

        left, right, prefix, exp10, priority = self._dataForOperator(other)
        return MassUnit(left + right, prefix=prefix, exp10=exp10, priority=priority)

    def __sub__(self, other):
        if not isinstance(other, MassUnit):
            return super().__sub__(other)

        left, right, prefix, exp10, priority = self._dataForOperator(other)
        return MassUnit(left - right, prefix=prefix, exp10=exp10, priority=priority)

    def _multByNumber(self, other):
        return MassUnit(self._value * other, prefix=self._prefix, exp10=self._exp10, priority=self._priority)


a = LengthUnit(15)
b = MassUnit(8)

print(a, a.value(new_prefix=""))
print(b, b.value(new_prefix=""))
print(a*a*a*b*2, (a*a*a*b*b*2).value())
