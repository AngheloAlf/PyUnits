from __future__ import annotations

from typing import Union, Optional
NumberType = Union[int, float]

from ..unitRepresentation.Units import BaseUnit


class DimensionLessUnit(BaseUnit):
    def __init__(self, value: NumberType, *, prefix: str="", exp10: int=0, priority: Optional[bool]=None):
        super().__init__(value, prefix=prefix, exp10=exp10, priority=priority, default_prefix="", unit="_")

    def getClass(self):
        return DimensionLessUnit

class LengthUnit(BaseUnit):
    def __init__(self, value: NumberType, *, prefix: str="", exp10: int=0, priority: Optional[bool]=None):
        super().__init__(value, prefix=prefix, exp10=exp10, priority=priority, default_prefix="", unit="m")

    def getClass(self):
        return LengthUnit

class MassUnit(BaseUnit):
    def __init__(self, value: NumberType, *, prefix: str="k", exp10: int=0, priority: Optional[bool]=None):
        super().__init__(value, prefix=prefix, exp10=exp10, priority=priority, default_prefix="k", unit="g")

    def getClass(self):
        return MassUnit

class TemperatureUnit(BaseUnit):
    def __init__(self, value: NumberType, *, prefix: str="", exp10: int=0, priority: Optional[bool]=None):
        super().__init__(value, prefix=prefix, exp10=exp10, priority=priority, default_prefix="", unit="K")

    def getClass(self):
        return TemperatureUnit

class TimeUnit(BaseUnit):
    def __init__(self, value: NumberType, *, prefix: str="", exp10: int=0, priority: Optional[bool]=None):
        super().__init__(value, prefix=prefix, exp10=exp10, priority=priority, default_prefix="", unit="s")

    def getClass(self):
        return TimeUnit

class SubstanceUnit(BaseUnit):
    def __init__(self, value: NumberType, *, prefix: str="", exp10: int=0, priority: Optional[bool]=None):
        super().__init__(value, prefix=prefix, exp10=exp10, priority=priority, default_prefix="", unit="mol")

    def getClass(self):
        return SubstanceUnit

class ElectricCurrentUnit(BaseUnit):
    def __init__(self, value: NumberType, *, prefix: str="", exp10: int=0, priority: Optional[bool]=None):
        super().__init__(value, prefix=prefix, exp10=exp10, priority=priority, default_prefix="", unit="A")

    def getClass(self):
        return ElectricCurrentUnit

class LuminousIntensityUnit(BaseUnit):
    def __init__(self, value: NumberType, *, prefix: str="", exp10: int=0, priority: Optional[bool]=None):
        super().__init__(value, prefix=prefix, exp10=exp10, priority=priority, default_prefix="", unit="cd")

    def getClass(self):
        return LuminousIntensityUnit
