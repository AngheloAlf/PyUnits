from __future__ import annotations

from numbers import Number

from . import SIUnits
from ..prefixes import SIPrefixes


def celsiusUnit(value: Number, *, power: Number=1):
    return SIUnits.kelvinUnit(value + 273.15, power=power)

def hertzUnit(value: Number, *, exp10: int=0, prefix: str="", power: Number=1):
    exp = SIPrefixes.magnitudeFactor(prefix, "")*power + exp10
    return value/SIUnits.secondUnit(1, exp10=-exp, power=power)

def newtonUnit(value: Number, *, exp10: int=0, prefix: str="", power: Number=1):
    exp = SIPrefixes.magnitudeFactor(prefix, "")*power + exp10
    result = SIUnits.kilogramUnit(value, power=power) * SIUnits.meterUnit(1, exp10=exp, power=power)
    result /= SIUnits.secondUnit(1, power=2*power)
    return result

def pascalUnit(value: Number, *, exp10: int=0, prefix: str="", power: Number=1):
    exp = SIPrefixes.magnitudeFactor(prefix, "")*power + exp10
    result = SIUnits.kilogramUnit(value, exp10=exp, power=power) / SIUnits.meterUnit(1, power=power)
    result /= SIUnits.secondUnit(1, power=2*power)
    return result

def jouleUnit(value: Number, *, exp10: int=0, prefix: str="", power: Number=1):
    exp = SIPrefixes.magnitudeFactor(prefix, "")*power + exp10
    result = SIUnits.kilogramUnit(value, power=power) * SIUnits.meterUnit(1, exp10=exp, power=2*power)
    result /= SIUnits.secondUnit(1, power=2*power)
    return result

def wattUnit(value: Number, *, exp10: int=0, prefix: str="", power: Number=1):
    exp = SIPrefixes.magnitudeFactor(prefix, "")*power + exp10
    result = SIUnits.kilogramUnit(value, power=power) * SIUnits.meterUnit(1, exp10=exp, power=2*power)
    result /= SIUnits.secondUnit(1, power=3*power)
    return result

def coulombUnit(value: Number, *, exp10: int=0, prefix: str="", power: Number=1):
    exp = SIPrefixes.magnitudeFactor(prefix, "")*power + exp10
    result = SIUnits.secondUnit(value, power=power) * SIUnits.ampereUnit(1, exp10=exp, power=power)
    return result

def voltUnit(value: Number, *, exp10: int=0, prefix: str="", power: Number=1):
    exp = SIPrefixes.magnitudeFactor(prefix, "")*power + exp10
    result = SIUnits.kilogramUnit(value, power=power) * SIUnits.meterUnit(1, exp10=exp, power=2*power)
    result /= SIUnits.secondUnit(1, power=3*power) * SIUnits.ampereUnit(1, power=power)
    return result

def faradUnit(value: Number, *, exp10: int=0, prefix: str="", power: Number=1):
    exp = SIPrefixes.magnitudeFactor(prefix, "")*power + exp10
    result = coulombUnit(value, exp10=exp, power=power) / voltUnit(1, power=power)
    return result

def ohmUnit(value: Number, *, exp10: int=0, prefix: str="", power: Number=1):
    exp = SIPrefixes.magnitudeFactor(prefix, "")*power + exp10
    result = voltUnit(value, exp10=exp, power=power) / SIUnits.ampereUnit(1, power=power)
    return result

def siemensUnit(value: Number, *, exp10: int=0, prefix: str="", power: Number=1):
    exp = SIPrefixes.magnitudeFactor(prefix, "")*power + exp10
    result = value / ohmUnit(1, exp10=-exp, power=power)
    return result

def weberUnit(value: Number, *, exp10: int=0, prefix: str="", power: Number=1):
    exp = SIPrefixes.magnitudeFactor(prefix, "")*power + exp10
    result = jouleUnit(value, exp10=exp, power=power) / SIUnits.ampereUnit(1, power=power)
    return result

def teslaUnit(value: Number, *, exp10: int=0, prefix: str="", power: Number=1):
    exp = SIPrefixes.magnitudeFactor(prefix, "")*power + exp10
    result = SIUnits.kilogramUnit(value, exp10=exp, power=power) / SIUnits.ampereUnit(1, power=power)
    result /= SIUnits.secondUnit(1, power=2*power)
    return result

def henryUnit(value: Number, *, exp10: int=0, prefix: str="", power: Number=1):
    exp = SIPrefixes.magnitudeFactor(prefix, "")*power + exp10
    result = voltUnit(value, exp10=power, power=power) * SIUnits.secondUnit(1, power=power)
    result /= SIUnits.ampereUnit(1, power=power)
    return result
