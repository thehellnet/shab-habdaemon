import logging
import threading

import serial

from gpsparser.gpsparser import parse_gga, parse_rmc


class SerialPort:
    logger = logging.getLogger("SerialPort")

    PORT = "/dev/ttyAMA0"
    BAUDRATE = 9600
    BYTESIZE = serial.EIGHTBITS
    PARITY = serial.PARITY_NONE
    STOPBITS = serial.STOPBITS_ONE
    XONXOFF = False
    RTSCTS = False
    DSRDTR = False
    TIMEOUT = 3
    WRITE_TIMEOUT = None
    INTER_BYTE_TIMEOUT = None

    def __init__(self, context):
        self._context = context
        self._serial = None
        self._thread = None
        self._keep_running = False

    def start(self):
        self.logger.info("Starting Serial Port")
        self._serial = serial.Serial()
        self._serial.setPort(self.PORT)
        self._serial.setBaudrate(self.BAUDRATE)
        self._serial.setByteSize(self.BYTESIZE)
        self._serial.setParity(self.PARITY)
        self._serial.setStopbits(self.STOPBITS)
        self._serial.setTimeout(self.TIMEOUT)
        self._serial.setXonXoff(self.XONXOFF)
        self._serial.setTimeout(self.TIMEOUT)
        self._serial.setWriteTimeout(self.WRITE_TIMEOUT)
        self._serial.setInterCharTimeout(self.INTER_BYTE_TIMEOUT)
        self._serial.open()

        self._thread = threading.Thread(target=self.read)
        self._thread.setDaemon(True)
        self._thread.start()

    def stop(self):
        self.logger.info("Stopping Serial Port")
        self._keep_running = False
        self._serial.close()
        self._thread.join()

    def read(self):
        self._keep_running = True

        while self._keep_running:
            try:
                line = self._serial.readline().strip()
            except OSError:
                continue

            self.logger.debug("Reading line: %s" % line)

            try:
                if line[:6] == "$GPGGA":
                    data = parse_gga(line)
                    if data is not None:
                        status, latitude, longitude, altitude = data
                        self.logger.debug(
                            "GPS FIX Status: %d - Setting position: %f %f %f" % (status, latitude, longitude, altitude))
                        self._context.fix_status = status
                        self._context.set_position((latitude, longitude, altitude))
                elif line[:6] == "$GPRMC":
                    gpsdatetime = parse_rmc(line)
                    if gpsdatetime is not None:
                        self.logger.debug("Setting GPS datetime: %s" % gpsdatetime)
                        self._context.gpsdatetime = gpsdatetime
            except ValueError:
                continue

    def write(self, line=""):
        if line is None or len(line) == 0:
            return

        data = line.strip()
        self.logger.debug("Writing line: %s" % data)
        print data
        self._serial.write(data + "\n")
        # self._serial.drainOutput()
