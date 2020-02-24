from __future__ import annotations

from ..TypesHelper import Number_t
from . import BaseQuantities
from ..unitRepresentation import Units
from ..prefixes import SIPrefixes


def meterUnit(value: Number_t, *, exp10: int=0, prefix: str="", power: Number_t=1):
    unit = BaseQuantities.LengthUnit(power=power)
    exp = SIPrefixes.magnitudeFactor(prefix, unit.defaultPrefix)*power + exp10
    if not isinstance(exp, int):
        raise RuntimeError()
    return Units.ValueUnits(value, unit, exp)

def centimeterUnit(value: Number_t, *, exp10: int=0, power: Number_t=1):
    return meterUnit(value, exp10=exp10, prefix="c", power=power)
def millimeterUnit(value: Number_t, *, exp10: int=0, power: Number_t=1):
    return meterUnit(value, exp10=exp10, prefix="m", power=power)
def kilometerUnit(value: Number_t, *, exp10: int=0, power: Number_t=1):
    return meterUnit(value, exp10=exp10, prefix="k", power=power)

def hectareUnit(value: Number_t, *, exp10: int=0):
    result = meterUnit(value, exp10=exp10+4, power=2)
    return result
def litreUnit(value: Number_t, *, exp10: int=0):
    result = meterUnit(value, exp10=exp10-3, power=3)
    return result


def gramUnit(value: Number_t, *, exp10: int=0, prefix: str="", power: Number_t=1):
    unit = BaseQuantities.MassUnit(power=power)
    exp = SIPrefixes.magnitudeFactor(prefix, unit.defaultPrefix)*power + exp10
    if not isinstance(exp, int):
        raise RuntimeError()
    return Units.ValueUnits(value, unit, exp10)

def kilogramUnit(value: Number_t, *, exp10: int=0, power: Number_t=1):
    return gramUnit(value, prefix="k", exp10=exp10, power=power)
def tonneUnit(value: Number_t, *, exp10: int=0, power: Number_t=1):
    return kilogramUnit(value, exp10=exp10+3, power=power)


def kelvinUnit(value: Number_t, *, exp10: int=0, prefix: str="", power: Number_t=1):
    unit = BaseQuantities.TemperatureUnit(power=power)
    exp = SIPrefixes.magnitudeFactor(prefix, unit.defaultPrefix)*power + exp10
    if not isinstance(exp, int):
        raise RuntimeError()
    return Units.ValueUnits(value, unit, exp10)


def secondUnit(value: Number_t, *, exp10: int=0, prefix: str="", power: Number_t=1):
    unit = BaseQuantities.TimeUnit(power=power)
    exp = SIPrefixes.magnitudeFactor(prefix, unit.defaultPrefix)*power + exp10
    if not isinstance(exp, int):
        raise RuntimeError()
    return Units.ValueUnits(value, unit, exp10)

def minuteUnit(value: Number_t, *, exp10: int=0, power: Number_t=1):
    return secondUnit(value*60, exp10=exp10, power=power)
def hourUnit(value: Number_t, *, exp10: int=0, power: Number_t=1):
    return minuteUnit(value*60, exp10=exp10, power=power)
def dayUnit(value: Number_t, *, exp10: int=0, power: Number_t=1):
    return hourUnit(value*24, exp10=exp10, power=power)


def molUnit(value: Number_t, *, exp10: int=0, prefix: str="", power: Number_t=1):
    unit = BaseQuantities.SubstanceUnit(power=power)
    exp = SIPrefixes.magnitudeFactor(prefix, unit.defaultPrefix)*power + exp10
    if not isinstance(exp, int):
        raise RuntimeError()
    return Units.ValueUnits(value, unit, exp10)


def ampereUnit(value: Number_t, *, exp10: int=0, prefix: str="", power: Number_t=1):
    unit = BaseQuantities.ElectricCurrentUnit(power=power)
    exp = SIPrefixes.magnitudeFactor(prefix, unit.defaultPrefix)*power + exp10
    if not isinstance(exp, int):
        raise RuntimeError()
    return Units.ValueUnits(value, unit, exp10)


def candelaUnit(value: Number_t, *, exp10: int=0, prefix: str="", power: Number_t=1):
    unit = BaseQuantities.LuminousIntensityUnit(power=power)
    exp = SIPrefixes.magnitudeFactor(prefix, unit.defaultPrefix)*power + exp10
    if not isinstance(exp, int):
        raise RuntimeError()
    return Units.ValueUnits(value, unit, exp10)
