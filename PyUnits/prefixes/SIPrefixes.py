si_prefixes = {"Y": 24, "Z": 21, "E": 18, "P": 15, "T": 12, "G": 9, "M": 6, "k": 3, "h": 2, "da": 1,
               "d": -1, "c": -2, "m": -3, "μ": -6, "n": -9, "p": -12, "f": -15, "a": -18, "z": -21, "y": -24}

def getExponentFromSIPrefix(symbol: str) -> int:
    return si_prefixes.get(symbol, 0)

def magnitudeFactor(symbol_from: str, symbol_to: str) -> int:
    return getExponentFromSIPrefix(symbol_from) - getExponentFromSIPrefix(symbol_to)

def isValidPrefix(symbol: str) -> bool:
    return symbol == "" or symbol in si_prefixes
