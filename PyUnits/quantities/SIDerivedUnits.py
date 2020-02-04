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
