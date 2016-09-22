import time

from protocol.abstractline import AbstractLine


class HabPosition(AbstractLine):
    def __init__(self, info=None):
        self._fix_status = 0
        self._latitude = 0
        self._longitude = 0
        self._altitude = 0

        if info is not None:
            self._fix_status, self._latitude, self._longitude, self._altitude = info

    def serialize_line(self):
        return "HP|%d|%d|%f|%f|%f" % (time.time() * 1000,
                                      self._fix_status,
                                      self._latitude,
                                      self._longitude,
                                      self._altitude)
