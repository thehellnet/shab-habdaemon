from image.imageparser import ImageParser
from protocol.habimage import HabImage
from protocol.habposition import HabPosition
from protocol.habtelemetry import HabTelemetry


class Action:
    def __init__(self, context, serialport):
        self._context = context
        self._serialport = serialport
        self._image_parser = ImageParser()

    def do_position(self):
        info = self._context.get_info_hab_position()
        line = HabPosition(info=info)
        self._serialport.write(line.serialize())

    def do_telemetry(self):
        info = self._context.get_info_hab_telemetry()
        line = HabTelemetry(info)
        self._serialport.write(line.serialize())

    def do_image(self):
        info = self._image_parser.thumb()
        line = HabImage(info=info)
        self._serialport.write(line.serialize())
