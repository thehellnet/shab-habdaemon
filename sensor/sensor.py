import smbus

from mpl3115a2 import MPL3115A2
from tmp102 import TMP102


class Sensor:
    def __init__(self):
        self._smbus = smbus.SMBus(1)
        self._tmp102 = TMP102(self._smbus)
        self._mpl3115a2 = MPL3115A2(self._smbus)

        self._mpl3115a2.init()

    def int_temp(self):
        return self._tmp102.temp()

    def ext_temp(self):
        return self._mpl3115a2.temperature()

    def ext_alt(self):
        return self._mpl3115a2.altitude()
