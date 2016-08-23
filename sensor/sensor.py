import logging
import smbus
import threading

from mpl3115a2 import MPL3115A2
from tmp102 import TMP102


class Sensor:
    logger = logging.getLogger("Sensor")

    def __init__(self, context):
        self._context = context
        self._thread = None
        self._keep_running = False

        self._smbus = smbus.SMBus(1)

        self._tmp102 = TMP102(self._smbus)

        self._mpl3115a2 = MPL3115A2(self._smbus)
        self._mpl3115a2.init()

    def start(self):
        self.logger.info("Starting")

        self._thread = threading.Thread(target=self.read)
        self._thread.setDaemon(True)
        self._thread.start()

    def stop(self):
        self.logger.info("Stopping")
        self._keep_running = False
        self._thread.join()

    def read(self):
        self._keep_running = True

        while self._keep_running:
            self._context.int_temp = self._tmp102.temp()
            self._context.ext_temp = self._mpl3115a2.temperature()
            self._context.ext_alt = self._mpl3115a2.altitude()
