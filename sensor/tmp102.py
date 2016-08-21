class TMP102:
    ADDRESS = 0x48

    def __init__(self, smbus):
        self._smbus = smbus
        pass

    def temp(self):
        rawdata = self._smbus.read_word_data(TMP102.ADDRESS, 0)
        low = (rawdata & 0xff00) >> 8
        high = (rawdata & 0x00ff)
        return (((high * 256) + low) >> 4) * 0.0625
