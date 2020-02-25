from PyUnits import SIUnits, SIDerivedUnits, ImperialUnits

a = SIUnits.meterUnit(15)
b = SIUnits.kilogramUnit(8, exp10=2)
c = SIUnits.secondUnit(2)

print(b, b%6)
print(a, a/4, a//4)

n = a*b/(c*c)
print(n)
print(a, float(a))
print(n, float(n))

test = n + n
print(test)

print(SIDerivedUnits.celsiusUnit(20))
print(ImperialUnits.fahrenheitUnit(68))

print(SIDerivedUnits.hertzUnit(20))
print(SIDerivedUnits.newtonUnit(30))

print(SIUnits.litreUnit(4000))


print(ImperialUnits.mileUnit(25))
print(ImperialUnits.perchUnit(10))
print(ImperialUnits.roodUnit(1))
print(float(ImperialUnits.roodUnit(1)))

print(SIUnits.meterUnit(2) - SIUnits.centimeterUnit(1))
