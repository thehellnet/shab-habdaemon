def checksum16(inputdata=""):
    if inputdata is None or len(inputdata) == 0:
        return None

    sum = 0
    for c in inputdata:
        sum += ord(c)
        sum %= 0xFFFF

    return sum
