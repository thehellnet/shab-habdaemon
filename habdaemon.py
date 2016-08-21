import logging
from datetime import datetime

from action import Action
from context import HabContext
from serialport.serialport import SerialPort
from sysupdate.sysupdate import SysUpdate

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("exifread").setLevel(logging.WARN)
logging.getLogger("SerialPort").setLevel(logging.DEBUG)
logging.getLogger("ImageParser").setLevel(logging.WARN)

logger = logging.getLogger()

keep_running = True
last_second = 0

logger.info("START")

logger.info("Creating context")
context = HabContext()

logger.info("Configuring serial port")
serialport = SerialPort(context=context)
serialport.start()

logger.info("Running system updater")
sysupdate = SysUpdate(context=context)
sysupdate.start()

logger.info("Preparing Actions")
action = Action(context, serialport)

logger.info("Running")
try:
    while keep_running:
        now = datetime.now()
        if now.second != last_second:
            last_second = now.second
            if now.second % 5 == 0:
                action.do_position()
            elif now.second % 2 == 0:
                action.do_telemetry()
        else:
            action.do_image()
except KeyboardInterrupt:
    pass

logger.info("Stopping")
sysupdate.stop()
serialport.stop()

logger.info("END")
