from __future__ import annotations

from typing import Union, Optional
NumberType = Union[int, float]

from . import SIUnits


def fahrenheitUnit(value: NumberType, *, exp10: int=0, priority: Optional[bool]=None):
    return SIUnits.kelvinUnit((value*(10**exp10) - 32)*5/9 + 273.15, prefix="", exp10=0, priority=priority)


def thouUnit(value: NumberType, *, exp10: int=0, priority: Optional[bool]=None):
    return SIUnits.meterUnit(25.4 * value, prefix="μ", exp10=exp10, priority=priority)
def inchUnit(value: NumberType, *, exp10: int=0, priority: Optional[bool]=None):
    return SIUnits.centimeterUnit(254 * value / 100, exp10=exp10, priority=priority)
def footUnit(value: NumberType, *, exp10: int=0, priority: Optional[bool]=None):
    return inchUnit(12 * value, exp10=exp10, priority=priority)
def yardUnit(value: NumberType, *, exp10: int=0, priority: Optional[bool]=None):
    return SIUnits.meterUnit(9144 * value / 10000, exp10=exp10, priority=priority)
def chainUnit(value: NumberType, *, exp10: int=0, priority: Optional[bool]=None):
    return yardUnit(22 * value, exp10=exp10, priority=priority)
def furlongUnit(value: NumberType, *, exp10: int=0, priority: Optional[bool]=None):
    return chainUnit(10 * value, exp10=exp10, priority=priority)
def mileUnit(value: NumberType, *, exp10: int=0, priority: Optional[bool]=None):
    return SIUnits.kilometerUnit(1609344 * value / 1000000, exp10=exp10, priority=priority)

def perchUnit(value: NumberType, *, exp10: int=0, priority: Optional[bool]=None):
    mul = 5.0292
    result = SIUnits.meterUnit(mul, priority=priority)
    result *= SIUnits.meterUnit(mul, exp10=exp10, priority=priority)
    result *= value
    return result
def roodUnit(value: NumberType, *, exp10: int=0, priority: Optional[bool]=None):
    mul = 5.0292
    result = SIUnits.meterUnit(40*mul, priority=priority)
    result *= SIUnits.meterUnit(mul, exp10=exp10, priority=priority)
    result *= value
    return result
def acreUnit(value: NumberType, *, exp10: int=0, priority: Optional[bool]=None):
    mul = 5.0292
    result = SIUnits.meterUnit(40*mul, priority=priority)
    result *= SIUnits.meterUnit(4*mul, exp10=exp10, priority=priority)
    result *= value
    return result


def poundUnit(value: NumberType, *, exp10: int=0, priority: Optional[bool]=None):
    return SIUnits.kilogramUnit(value * 0.45359237, exp10=exp10, priority=priority)
