from __future__ import annotations

from typing import Union, Optional
NumberType = Union[int, float]

from . import BaseQuantities


def meterUnit(value: NumberType, *, prefix: str="", exp10: int=0, priority: Optional[bool]=None):
    return BaseQuantities.LengthUnit(value, prefix=prefix, exp10=exp10, priority=priority)

def centimeterUnit(value: NumberType, *, exp10: int=0, priority: Optional[bool]=None):
    return MeterUnit(value, prefix="c", exp10=exp10, priority=priority)
def millimeterUnit(value: NumberType, *, exp10: int=0, priority: Optional[bool]=None):
    return MeterUnit(value, prefix="m", exp10=exp10, priority=priority)
def kilometerUnit(value: NumberType, *, exp10: int=0, priority: Optional[bool]=None):
    return MeterUnit(value, prefix="k", exp10=exp10, priority=priority)


def gramUnit(value: NumberType, *, prefix: str="", exp10: int=0, priority: Optional[bool]=None):
    return BaseQuantities.MassUnit(value, prefix=prefix, exp10=exp10, priority=priority)

def kilogramUnit(value: NumberType, *, exp10: int=0, priority: Optional[bool]=None):
    return gramUnit(value, prefix="k", exp10=exp10, priority=priority)


def kelvinUnit(value: NumberType, *, prefix: str="", exp10: int=0, priority: Optional[bool]=None):
    return BaseQuantities.TemperatureUnit(value, prefix=prefix, exp10=exp10, priority=priority)


def secondUnit(value: NumberType, *, prefix: str="", exp10: int=0, priority: Optional[bool]=None):
    return BaseQuantities.TimeUnit(value, prefix=prefix, exp10=exp10, priority=priority)

def minuteUnit(value: NumberType, *, prefix: str="", exp10: int=0, priority: Optional[bool]=None):
    return secondUnit(value*60, prefix=prefix, exp10=exp10, priority=priority)
def hourUnit(value: NumberType, *, prefix: str="", exp10: int=0, priority: Optional[bool]=None):
    return minuteUnit(value*60, prefix=prefix, exp10=exp10, priority=priority)
def dayUnit(value: NumberType, *, prefix: str="", exp10: int=0, priority: Optional[bool]=None):
    return hourUnit(value*24, prefix=prefix, exp10=exp10, priority=priority)


def molUnit(value: NumberType, *, prefix: str="", exp10: int=0, priority: Optional[bool]=None):
    return BaseQuantities.SubstanceUnit(value, prefix=prefix, exp10=exp10, priority=priority)


def ampereUnit(value: NumberType, *, prefix: str="", exp10: int=0, priority: Optional[bool]=None):
    return BaseQuantities.ElectricCurrentUnit(value, prefix=prefix, exp10=exp10, priority=priority)


def candelaUnit(value: NumberType, *, prefix: str="", exp10: int=0, priority: Optional[bool]=None):
    return BaseQuantities.LuminousIntensityUnit(value, prefix=prefix, exp10=exp10, priority=priority)
