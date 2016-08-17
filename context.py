import logging
from datetime import datetime


class HabContext:
    def __init__(self):
        self.latitude = 0
        self.longitude = 0
        self.altitude = 0
        self.gpsdatetime = datetime.now()

    def set_position(self, position):
        (self.latitude, self.longitude, self.altitude) = position
