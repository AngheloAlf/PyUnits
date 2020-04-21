from PyUnits.unitRepresentation.Units__ import *


m = Unit("m")
print(m.copy())
m2 = UnitHandler(m, prefix="k", power=2)
print(f'{m2} == {m2.changePrefix("c")}')




print(FractionUnits(m, m2))
# print(FractionUnits(m, m2**2))
