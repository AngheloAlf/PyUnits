from __future__ import annotations

from typing import Union, Optional
NumberType = Union[int, float]

from . import SIUnits
from ..prefixes import SIPrefixes


def celsiusUnit(value: NumberType, *, prefix: str="", exp10: int=0, priority: Optional[bool]=None):
    exp = SIPrefixes.magnitudeFactor(prefix, "") + exp10
    return SIUnits.kelvinUnit(value*(10**exp) + 273.15, prefix="", exp10=0, priority=priority)

def hertzUnit(value: NumberType, *, prefix: str="", exp10: int=0, priority: Optional[bool]=None):
    return 1/SIUnits.secondUnit(value, prefix=prefix, exp10=exp10, priority=priority)

def newtonUnit(value: NumberType, *, prefix: str="", exp10: int=0, priority: Optional[bool]=None):
    exp = SIPrefixes.magnitudeFactor(prefix, "") + exp10
    value = value*(10**exp)
    result = SIUnits.kilogramUnit(1, priority=priority) * SIUnits.meterUnit(1, priority=priority)
    result /= SIUnits.secondUnit(1, priority=priority) * SIUnits.secondUnit(1, priority=priority)
    result *= value
    return result

def pascalUnit(value: NumberType, *, prefix: str="", exp10: int=0, priority: Optional[bool]=None):
    exp = SIPrefixes.magnitudeFactor(prefix, "") + exp10
    value = value*(10**exp)
    result = SIUnits.kilogramUnit(1, priority=priority) / SIUnits.meterUnit(1, priority=priority)
    result /= SIUnits.secondUnit(1, priority=priority) * SIUnits.secondUnit(1, priority=priority)
    result *= value
    return result

def jouleUnit(value: NumberType, *, prefix: str="", exp10: int=0, priority: Optional[bool]=None):
    exp = SIPrefixes.magnitudeFactor(prefix, "") + exp10
    value = value*(10**exp)
    result = SIUnits.kilogramUnit(1, priority=priority) * SIUnits.meterUnit(1, priority=priority) * SIUnits.meterUnit(1, priority=priority)
    result /= SIUnits.secondUnit(1, priority=priority) * SIUnits.secondUnit(1, priority=priority)
    result *= value
    return result

def wattUnit(value: NumberType, *, prefix: str="", exp10: int=0, priority: Optional[bool]=None):
    exp = SIPrefixes.magnitudeFactor(prefix, "") + exp10
    value = value*(10**exp)
    result = SIUnits.kilogramUnit(1, priority=priority) * SIUnits.meterUnit(1, priority=priority) * SIUnits.meterUnit(1, priority=priority)
    result /= SIUnits.secondUnit(1, priority=priority) * SIUnits.secondUnit(1, priority=priority) * SIUnits.secondUnit(1, priority=priority)
    result *= value
    return result

def coulombUnit(value: NumberType, *, prefix: str="", exp10: int=0, priority: Optional[bool]=None):
    exp = SIPrefixes.magnitudeFactor(prefix, "") + exp10
    value = value*(10**exp)
    result = SIUnits.secondUnit(1, priority=priority) * SIUnits.ampereUnit(1, priority=priority)
    result *= value
    return result

def voltUnit(value: NumberType, *, prefix: str="", exp10: int=0, priority: Optional[bool]=None):
    exp = SIPrefixes.magnitudeFactor(prefix, "") + exp10
    value = value*(10**exp)
    result = SIUnits.kilogramUnit(1, priority=priority) * SIUnits.meterUnit(1, priority=priority) * SIUnits.meterUnit(1, priority=priority)
    result /= SIUnits.secondUnit(1, priority=priority) * SIUnits.secondUnit(1, priority=priority) * SIUnits.secondUnit(1, priority=priority) * SIUnits.ampereUnit(1, priority=priority)
    result *= value
    return result

def faradUnit(value: NumberType, *, prefix: str="", exp10: int=0, priority: Optional[bool]=None):
    exp = SIPrefixes.magnitudeFactor(prefix, "") + exp10
    value = value*(10**exp)
    result = coulombUnit(1, priority=priority) / voltUnit(1, priority=priority)
    result *= value
    return result

def ohmUnit(value: NumberType, *, prefix: str="", exp10: int=0, priority: Optional[bool]=None):
    exp = SIPrefixes.magnitudeFactor(prefix, "") + exp10
    value = value*(10**exp)
    result = voltUnit(1, priority=priority) / SIUnits.ampereUnit(1, priority=priority)
    result *= value
    return result

def siemensUnit(value: NumberType, *, prefix: str="", exp10: int=0, priority: Optional[bool]=None):
    exp = SIPrefixes.magnitudeFactor(prefix, "") + exp10
    value = value*(10**exp)
    result = 1 / ohmUnit(1, priority=priority)
    result *= value
    return result

def weberUnit(value: NumberType, *, prefix: str="", exp10: int=0, priority: Optional[bool]=None):
    exp = SIPrefixes.magnitudeFactor(prefix, "") + exp10
    value = value*(10**exp)
    result = jouleUnit(1, priority=priority) / SIUnits.ampereUnit(1, priority=priority)
    result *= value
    return result

def teslaUnit(value: NumberType, *, prefix: str="", exp10: int=0, priority: Optional[bool]=None):
    exp = SIPrefixes.magnitudeFactor(prefix, "") + exp10
    value = value*(10**exp)
    result = SIUnits.kilogramUnit(1, priority=priority) / SIUnits.ampereUnit(1, priority=priority)
    result /= SIUnits.secondUnit(1, priority=priority) * SIUnits.secondUnit(1, priority=priority)
    result *= value
    return result

def henryUnit(value: NumberType, *, prefix: str="", exp10: int=0, priority: Optional[bool]=None):
    exp = SIPrefixes.magnitudeFactor(prefix, "") + exp10
    value = value*(10**exp)
    result = voltUnit(1, priority=priority) * SIUnits.secondUnit(1, priority=priority)
    result /= SIUnits.ampereUnit(1, priority=priority)
    result *= value
    return result
