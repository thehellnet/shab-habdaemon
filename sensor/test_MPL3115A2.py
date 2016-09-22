import logging
import smbus
import sys
import time

from mpl3115a2 import MPL3115A2

logging.basicConfig(level=logging.DEBUG)

smbus = smbus.SMBus(1)
mpl3115a2 = MPL3115A2(smbus)
if not mpl3115a2.init():
    sys.exit(1)

while True:
    print mpl3115a2.altitude()
    print mpl3115a2.temperature()
    time.sleep(3)
