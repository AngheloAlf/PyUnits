from __future__ import annotations

from typing import Union, Optional
NumberType = Union[int, float]

from . import SIUnits
from ..prefixes import SIPrefixes


def fahrenheitUnit(value: NumberType, *, prefix: str="", exp10: int=0, priority: Optional[bool]=None):
    exp = SIPrefixes.magnitudeFactor(prefix, "") + exp10
    return SIUnits.kelvinUnit((value*(10**exp) - 32)*5/9 + 273.15, prefix="", exp10=0, priority=priority)
