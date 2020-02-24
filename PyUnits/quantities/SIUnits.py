from __future__ import annotations

from numbers import Number

from . import BaseQuantities
from ..unitRepresentation import Units
from ..prefixes import SIPrefixes


def meterUnit(value: Number, *, exp10: int=0, prefix: str="", power: Number=1):
    unit = BaseQuantities.LengthUnit(power=power)
    exp10 += SIPrefixes.magnitudeFactor(prefix, unit.defaultPrefix)*power
    return Units.ValueUnits(value, unit, exp10)

def centimeterUnit(value: Number, *, exp10: int=0, power: Number=1):
    return meterUnit(value, exp10=exp10, prefix="c", power=power)
def millimeterUnit(value: Number, *, exp10: int=0, power: Number=1):
    return meterUnit(value, exp10=exp10, prefix="m", power=power)
def kilometerUnit(value: Number, *, exp10: int=0, power: Number=1):
    return meterUnit(value, exp10=exp10, prefix="k", power=power)

def hectareUnit(value: Number, *, exp10: int=0):
    result = meterUnit(value, exp10=exp10+4, power=2)
    return result
def litreUnit(value: Number, *, exp10: int=0):
    result = meterUnit(value, exp10=exp10-3, power=3)
    return result


def gramUnit(value: Number, *, exp10: int=0, prefix: str="", power: Number=1):
    unit = BaseQuantities.MassUnit(power=power)
    exp10 += SIPrefixes.magnitudeFactor(prefix, unit.defaultPrefix)*power
    return Units.ValueUnits(value, unit, exp10)

def kilogramUnit(value: Number, *, exp10: int=0, power: Number=1):
    return gramUnit(value, prefix="k", exp10=exp10, power=power)
def tonneUnit(value: Number, *, exp10: int=0, power: Number=1):
    return kilogramUnit(value, exp10=exp10+3, power=power)


def kelvinUnit(value: Number, *, exp10: int=0, prefix: str="", power: Number=1):
    unit = BaseQuantities.TemperatureUnit(power=power)
    exp10 += SIPrefixes.magnitudeFactor(prefix, unit.defaultPrefix)*power
    return Units.ValueUnits(value, unit, exp10)


def secondUnit(value: Number, *, exp10: int=0, prefix: str="", power: Number=1):
    unit = BaseQuantities.TimeUnit(power=power)
    exp10 += SIPrefixes.magnitudeFactor(prefix, unit.defaultPrefix)*power
    return Units.ValueUnits(value, unit, exp10)

def minuteUnit(value: Number, *, exp10: int=0, power: Number=1):
    return secondUnit(value*60, exp10=exp10, power=power)
def hourUnit(value: Number, *, exp10: int=0, power: Number=1):
    return minuteUnit(value*60, exp10=exp10, power=power)
def dayUnit(value: Number, *, exp10: int=0, power: Number=1):
    return hourUnit(value*24, exp10=exp10, power=power)


def molUnit(value: Number, *, exp10: int=0, prefix: str="", power: Number=1):
    unit = BaseQuantities.SubstanceUnit(power=power)
    exp10 += SIPrefixes.magnitudeFactor(prefix, unit.defaultPrefix)*power
    return Units.ValueUnits(value, unit, exp10)


def ampereUnit(value: Number, *, exp10: int=0, prefix: str="", power: Number=1):
    unit = BaseQuantities.ElectricCurrentUnit(power=power)
    exp10 += SIPrefixes.magnitudeFactor(prefix, unit.defaultPrefix)*power
    return Units.ValueUnits(value, unit, exp10)


def candelaUnit(value: Number, *, exp10: int=0, prefix: str="", power: Number=1):
    unit = BaseQuantities.LuminousIntensityUnit(power=power)
    exp10 += SIPrefixes.magnitudeFactor(prefix, unit.defaultPrefix)*power
    return Units.ValueUnits(value, unit, exp10)
