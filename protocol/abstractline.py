import abc
import time

from protocol.utility import checksum16


class AbstractLine(object):
    __metaclass__ = abc.ABCMeta

    def serialize(self):
        line = self.serialize_line()
        if line is None or len(line) == 0:
            return None

        return "%0.4X|%s" % (checksum16(line), line)

    @abc.abstractmethod
    def serialize_line(self):
        return None
