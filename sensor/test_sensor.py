from unittest import TestCase

import logging

from sensor import Sensor


class TestSensor(TestCase):
    def test_int_temp(self):
        logging.basicConfig(level=logging.DEBUG)
        sensor = Sensor()
        print sensor.int_temp()
        print sensor.ext_temp()
        print sensor.ext_alt()