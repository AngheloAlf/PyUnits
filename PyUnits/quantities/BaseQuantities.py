from __future__ import annotations

from ..TypesHelper import Number_t
from ..unitRepresentation.Units import Unit


class DimensionLessUnit(Unit):
    def __new__(cls, *, power: Number_t=1):
        return super(DimensionLessUnit, cls).__new__(cls, unit="_", defaultPrefix="", power=power)
    def __init__(self, *, power: Number_t=1):
        super().__init__(unit="_", defaultPrefix="", power=power)

class LengthUnit(Unit):
    def __new__(cls, *, power: Number_t=1):
        return super(LengthUnit, cls).__new__(cls, unit="m", defaultPrefix="", power=power)
    def __init__(self, *, power: Number_t=1):
        super().__init__(unit="m", defaultPrefix="", power=power)

class MassUnit(Unit):
    def __new__(cls, *, power: Number_t=1):
        return super(MassUnit, cls).__new__(cls, unit="g", defaultPrefix="k", power=power)
    def __init__(self, *, power: Number_t=1):
        super().__init__(unit="g", defaultPrefix="k", power=power)

class TemperatureUnit(Unit):
    def __new__(cls, *, power: Number_t=1):
        return super(TemperatureUnit, cls).__new__(cls, unit="K", defaultPrefix="", power=power)
    def __init__(self, *, power: Number_t=1):
        super().__init__(unit="K", defaultPrefix="", power=power)

class TimeUnit(Unit):
    def __new__(cls, *, power: Number_t=1):
        return super(TimeUnit, cls).__new__(cls, unit="s", defaultPrefix="", power=power)
    def __init__(self, *, power: Number_t=1):
        super().__init__(unit="s", defaultPrefix="", power=power)

class SubstanceUnit(Unit):
    def __new__(cls, *, power: Number_t=1):
        return super(SubstanceUnit, cls).__new__(cls, unit="mol", defaultPrefix="", power=power)
    def __init__(self, *, power: Number_t=1):
        super().__init__(unit="mol", defaultPrefix="", power=power)

class ElectricCurrentUnit(Unit):
    def __new__(cls, *, power: Number_t=1):
        return super(ElectricCurrentUnit, cls).__new__(cls, unit="A", defaultPrefix="", power=power)
    def __init__(self, *, power: Number_t=1):
        super().__init__(unit="A", defaultPrefix="", power=power)

class LuminousIntensityUnit(Unit):
    def __new__(cls, *, power: Number_t=1):
        return super(LuminousIntensityUnit, cls).__new__(cls, unit="cd", defaultPrefix="", power=power)
    def __init__(self, *, power: Number_t=1):
        super().__init__(unit="cd", defaultPrefix="", power=power)
