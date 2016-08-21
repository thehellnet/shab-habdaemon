import logging
import os
import threading
from datetime import datetime
from time import sleep

from config import SYSUPDATE_UPDATE_INTERVAL


class SysUpdate:
    logger = logging.getLogger("SysUpdate")

    def __init__(self, context):
        self._context = context
        self._thread = None
        self._keep_running = False
        self._last_update = datetime.now()

    def start(self):
        self.logger.info("Starting system updater")
        self._thread = threading.Thread(target=self.update)
        self._thread.setDaemon(True)
        self._thread.start()

    def stop(self):
        self.logger.info("Stopping system updater")
        self._keep_running = False
        self._thread.join()

    def update(self):
        self._keep_running = True

        while self._keep_running:
            sleep(1)

            interval = datetime.now() - self._last_update
            if interval.seconds < SYSUPDATE_UPDATE_INTERVAL:
                continue

            self._last_update = datetime.now()
            if self._context.gpsdatetime is not None:
                self.logger.debug("Update system time")
                os.system("date --set=\"%s\"" % self._context.gpsdatetime)
