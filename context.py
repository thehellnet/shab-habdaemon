from datetime import datetime


class HabContext:
    def __init__(self):
        self.fix_status = 0
        self.latitude = 0
        self.longitude = 0
        self.altitude = 0
        self.gpsdatetime = datetime.now()
        self.int_temp = 0
        self.ext_temp = 0
        self.ext_alt = 0

    def set_position(self, position):
        self.latitude, self.longitude, self.altitude = position

    def get_info_hab_position(self):
        return self.fix_status, self.latitude, self.longitude, self.altitude

    def get_info_hab_telemetry(self):
        return self.int_temp, self.ext_temp, self.ext_alt
