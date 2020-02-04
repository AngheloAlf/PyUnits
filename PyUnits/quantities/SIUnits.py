from __future__ import annotations

from typing import Union, Optional
NumberType = Union[int, float]

from . import BaseQuantities


def MeterUnit(value: NumberType, *, prefix: str="", exp10: int=0, priority: Optional[bool]=None):
    return BaseQuantities.LengthUnit(value, prefix=prefix, exp10=exp10, priority=priority)

def CentimeterUnit(value: NumberType, *, exp10: int=0, priority: Optional[bool]=None):
    return MeterUnit(value, prefix="c", exp10=exp10, priority=priority)
def MillimeterUnit(value: NumberType, *, exp10: int=0, priority: Optional[bool]=None):
    return MeterUnit(value, prefix="m", exp10=exp10, priority=priority)
def KilometerUnit(value: NumberType, *, exp10: int=0, priority: Optional[bool]=None):
    return MeterUnit(value, prefix="k", exp10=exp10, priority=priority)


def GramUnit(value: NumberType, *, prefix: str="", exp10: int=0, priority: Optional[bool]=None):
    return BaseQuantities.MassUnit(value, prefix=prefix, exp10=exp10, priority=priority)

def KilogramUnit(value: NumberType, *, exp10: int=0, priority: Optional[bool]=None):
    return GramUnit(value, prefix="k", exp10=exp10, priority=priority)


def KelvinUnit(value: NumberType, *, prefix: str="", exp10: int=0, priority: Optional[bool]=None):
    return BaseQuantities.TemperatureUnit(value, prefix=prefix, exp10=exp10, priority=priority)


def SecondUnit(value: NumberType, *, prefix: str="", exp10: int=0, priority: Optional[bool]=None):
    return BaseQuantities.TimeUnit(value, prefix=prefix, exp10=exp10, priority=priority)

def MinuteUnit(value: NumberType, *, prefix: str="", exp10: int=0, priority: Optional[bool]=None):
    return SecondUnit(value*60, prefix=prefix, exp10=exp10, priority=priority)
def HourUnit(value: NumberType, *, prefix: str="", exp10: int=0, priority: Optional[bool]=None):
    return MinuteUnit(value*60, prefix=prefix, exp10=exp10, priority=priority)
def DayUnit(value: NumberType, *, prefix: str="", exp10: int=0, priority: Optional[bool]=None):
    return HourUnit(value*24, prefix=prefix, exp10=exp10, priority=priority)


def MolUnit(value: NumberType, *, prefix: str="", exp10: int=0, priority: Optional[bool]=None):
    return BaseQuantities.SubstanceUnit(value, prefix=prefix, exp10=exp10, priority=priority)


def AmpereUnit(value: NumberType, *, prefix: str="", exp10: int=0, priority: Optional[bool]=None):
    return BaseQuantities.ElectricCurrentUnit(value, prefix=prefix, exp10=exp10, priority=priority)


def CandelaUnit(value: NumberType, *, prefix: str="", exp10: int=0, priority: Optional[bool]=None):
    return BaseQuantities.LuminousIntensityUnit(value, prefix=prefix, exp10=exp10, priority=priority)
