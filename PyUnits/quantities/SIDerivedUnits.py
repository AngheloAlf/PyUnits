from __future__ import annotations

from ..TypesHelper import Number_t
from . import SIUnits
from ..prefixes import SIPrefixes


def celsiusUnit(value: Number_t, *, power: Number_t=1):
    return SIUnits.kelvinUnit(value + 273.15, power=power)

def hertzUnit(value: Number_t, *, exp10: int=0, prefix: str="", power: Number_t=1):
    exp = SIPrefixes.magnitudeFactor(prefix, "")*power + exp10
    if not isinstance(exp, int):
        raise RuntimeError()
    return value/SIUnits.secondUnit(1, exp10=-exp, power=power)

def newtonUnit(value: Number_t, *, exp10: int=0, prefix: str="", power: Number_t=1):
    exp = SIPrefixes.magnitudeFactor(prefix, "")*power + exp10
    if not isinstance(exp, int):
        raise RuntimeError()
    result = SIUnits.kilogramUnit(value, power=power) * SIUnits.meterUnit(1, exp10=exp, power=power)
    result /= SIUnits.secondUnit(1, power=2*power)
    return result

def pascalUnit(value: Number_t, *, exp10: int=0, prefix: str="", power: Number_t=1):
    exp = SIPrefixes.magnitudeFactor(prefix, "")*power + exp10
    if not isinstance(exp, int):
        raise RuntimeError()
    result = SIUnits.kilogramUnit(value, exp10=exp, power=power) / SIUnits.meterUnit(1, power=power)
    result /= SIUnits.secondUnit(1, power=2*power)
    return result

def jouleUnit(value: Number_t, *, exp10: int=0, prefix: str="", power: Number_t=1):
    exp = SIPrefixes.magnitudeFactor(prefix, "")*power + exp10
    if not isinstance(exp, int):
        raise RuntimeError()
    result = SIUnits.kilogramUnit(value, power=power) * SIUnits.meterUnit(1, exp10=exp, power=2*power)
    result /= SIUnits.secondUnit(1, power=2*power)
    return result

def wattUnit(value: Number_t, *, exp10: int=0, prefix: str="", power: Number_t=1):
    exp = SIPrefixes.magnitudeFactor(prefix, "")*power + exp10
    if not isinstance(exp, int):
        raise RuntimeError()
    result = SIUnits.kilogramUnit(value, power=power) * SIUnits.meterUnit(1, exp10=exp, power=2*power)
    result /= SIUnits.secondUnit(1, power=3*power)
    return result

def coulombUnit(value: Number_t, *, exp10: int=0, prefix: str="", power: Number_t=1):
    exp = SIPrefixes.magnitudeFactor(prefix, "")*power + exp10
    if not isinstance(exp, int):
        raise RuntimeError()
    result = SIUnits.secondUnit(value, power=power) * SIUnits.ampereUnit(1, exp10=exp, power=power)
    return result

def voltUnit(value: Number_t, *, exp10: int=0, prefix: str="", power: Number_t=1):
    exp = SIPrefixes.magnitudeFactor(prefix, "")*power + exp10
    if not isinstance(exp, int):
        raise RuntimeError()
    result = SIUnits.kilogramUnit(value, power=power) * SIUnits.meterUnit(1, exp10=exp, power=2*power)
    result /= SIUnits.secondUnit(1, power=3*power) * SIUnits.ampereUnit(1, power=power)
    return result

def faradUnit(value: Number_t, *, exp10: int=0, prefix: str="", power: Number_t=1):
    exp = SIPrefixes.magnitudeFactor(prefix, "")*power + exp10
    if not isinstance(exp, int):
        raise RuntimeError()
    result = coulombUnit(value, exp10=exp, power=power) / voltUnit(1, power=power)
    return result

def ohmUnit(value: Number_t, *, exp10: int=0, prefix: str="", power: Number_t=1):
    exp = SIPrefixes.magnitudeFactor(prefix, "")*power + exp10
    if not isinstance(exp, int):
        raise RuntimeError()
    result = voltUnit(value, exp10=exp, power=power) / SIUnits.ampereUnit(1, power=power)
    return result

def siemensUnit(value: Number_t, *, exp10: int=0, prefix: str="", power: Number_t=1):
    exp = SIPrefixes.magnitudeFactor(prefix, "")*power + exp10
    if not isinstance(exp, int):
        raise RuntimeError()
    result = value / ohmUnit(1, exp10=-exp, power=power)
    return result

def weberUnit(value: Number_t, *, exp10: int=0, prefix: str="", power: Number_t=1):
    exp = SIPrefixes.magnitudeFactor(prefix, "")*power + exp10
    if not isinstance(exp, int):
        raise RuntimeError()
    result = jouleUnit(value, exp10=exp, power=power) / SIUnits.ampereUnit(1, power=power)
    return result

def teslaUnit(value: Number_t, *, exp10: int=0, prefix: str="", power: Number_t=1):
    exp = SIPrefixes.magnitudeFactor(prefix, "")*power + exp10
    if not isinstance(exp, int):
        raise RuntimeError()
    result = SIUnits.kilogramUnit(value, exp10=exp, power=power) / SIUnits.ampereUnit(1, power=power)
    result /= SIUnits.secondUnit(1, power=2*power)
    return result

def henryUnit(value: Number_t, *, exp10: int=0, prefix: str="", power: Number_t=1):
    exp = SIPrefixes.magnitudeFactor(prefix, "")*power + exp10
    if not isinstance(exp, int):
        raise RuntimeError()
    result = voltUnit(value, exp10=exp, power=power) * SIUnits.secondUnit(1, power=power)
    result /= SIUnits.ampereUnit(1, power=power)
    return result
