from protocol.abstractline import AbstractLine


class HabTelemetry(AbstractLine):
    def __init__(self, info=None):
        self._int_temp = 0
        self._ext_temp = 0
        self._ext_alt = 0

        if info is not None:
            self._int_temp, self._ext_temp, self._ext_alt = info

    def serialize_line(self):
        return "HT|%.01f|%.01f|%d" % \
               (self._int_temp, self._ext_temp, self._ext_alt)
