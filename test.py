from PyUnits import SIUnits, SIDerivedUnits, ImperialUnits

a = SIUnits.meterUnit(15)
b = SIUnits.kilogramUnit(8)
c = SIUnits.secondUnit(2)

n = a*b/(c*c)
print(n)
# print(a, a.value())
# print(n, n.value())

test = n + n
print(test)

print(SIDerivedUnits.celsiusUnit(20))
print(ImperialUnits.fahrenheitUnit(68))

print(SIDerivedUnits.hertzUnit(20))
print(SIDerivedUnits.newtonUnit(30))

