import logging
import time

from context import HabContext
from serialport.serialport import SerialPort

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("SerialPort").setLevel(logging.WARN)

logger = logging.getLogger()

keep_running = True

logger.info("START")

logger.info("Creating context")
context = HabContext()

logger.info("Configuring serial port")
serialport = SerialPort(context=context)
serialport.start()

logger.info("Running")
try:
    while keep_running:
        time.sleep(3)

        logger.info("Loop")
        print "    >>>[TX]>>> Latitude: %f - Longitude: %f - Altitude: %f" \
              % (context.latitude, context.longitude, context.altitude)
        print "    >>>[TX]>>> Datetime: %s" % context.gpsdatetime

except KeyboardInterrupt:
    pass

logger.info("Stopping")
serialport.stop()

logger.info("END")
