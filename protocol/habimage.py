import base64

from protocol.abstractline import AbstractLine


class HabImage(AbstractLine):
    def __init__(self, info=None):
        self._slice_tot = 0
        self._slice_num = 0
        self._data = None

        if info is not None:
            self._slice_tot, self._slice_num, self._data = info

    def serialize_line(self):
        return "HI|%d|%d|%s" % \
               (self._slice_tot,
                self._slice_num,
                base64.urlsafe_b64encode(self._data))
