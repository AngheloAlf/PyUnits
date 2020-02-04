from PyUnits import SIUnits

a = SIUnits.MeterUnit(15)
b = SIUnits.KilogramUnit(8)
c = SIUnits.SecondUnit(2)

n = a*b/(c*c)
print(n)
# print(a, a.value())
# print(n, n.value())

test = n - n
print(n/n)
