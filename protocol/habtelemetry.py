from protocol.abstractline import AbstractLine


class HabTelemetry(AbstractLine):
    def __init__(self):
        pass

    def serialize_line(self):
        return "HT|"
