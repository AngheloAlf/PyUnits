from __future__ import annotations

from numbers import Number
from typing import Union, Optional

from . import SIUnits


def fahrenheitUnit(value: Number, *, power: Number=1):
    return SIUnits.kelvinUnit((value - 32)*5/9 + 273.15, power=power)


def thouUnit(value: Number, *, exp10: int=0, power: Number=1):
    return SIUnits.meterUnit(25.4 * value, prefix="μ", exp10=exp10, power=power)
def inchUnit(value: Number, *, exp10: int=0, power: Number=1):
    return SIUnits.centimeterUnit(254 * value / 100, exp10=exp10, power=power)
def footUnit(value: Number, *, exp10: int=0, power: Number=1):
    return inchUnit(12 * value, exp10=exp10, power=power)
def yardUnit(value: Number, *, exp10: int=0, power: Number=1):
    return SIUnits.meterUnit(9144 * value / 10000, exp10=exp10, power=power)
def chainUnit(value: Number, *, exp10: int=0, power: Number=1):
    return yardUnit(22 * value, exp10=exp10, power=power)
def furlongUnit(value: Number, *, exp10: int=0, power: Number=1):
    return chainUnit(10 * value, exp10=exp10, power=power)
def mileUnit(value: Number, *, exp10: int=0, power: Number=1):
    return SIUnits.kilometerUnit(1609344 * value / 1000000, exp10=exp10, power=power)

def perchUnit(value: Number, *, exp10: int=0, power: Number=1):
    mul = 5.0292
    result = SIUnits.meterUnit(mul, power=power)
    result *= SIUnits.meterUnit(mul, exp10=exp10, power=power)
    result *= value
    return result
def roodUnit(value: Number, *, exp10: int=0, power: Number=1):
    mul = 5.0292
    result = SIUnits.meterUnit(40*mul, power=power)
    result *= SIUnits.meterUnit(mul, exp10=exp10, power=power)
    result *= value
    return result
def acreUnit(value: Number, *, exp10: int=0, power: Number=1):
    mul = 5.0292
    result = SIUnits.meterUnit(40*mul, power=power)
    result *= SIUnits.meterUnit(4*mul, exp10=exp10, power=power)
    result *= value
    return result


def poundUnit(value: Number, *, exp10: int=0, power: Number=1):
    return SIUnits.kilogramUnit(value * 0.45359237, exp10=exp10, power=power)
