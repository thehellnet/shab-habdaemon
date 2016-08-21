import datetime
import pytz


def parse_gga(line=""):
    if line is None or len(line) == 0:
        return None

    items = line.split(",")
    if len(items) != 15 \
            or items[0] != "$GPGGA":
        return None

    status = int(items[6])
    latitude = (float(items[2][:2]) + float(items[2][2:]) / 60) * (-1 if items[3] == "S" else 1)
    longitude = (float(items[4][:3]) + float(items[4][3:]) / 60) * (-1 if items[5] == "W" else 1)
    altitude = float(items[9])

    return status, latitude, longitude, altitude


def parse_rmc(line=""):
    if line is None or len(line) == 0:
        return None

    items = line.split(",")
    if len(items) != 13 \
            or items[0] != "$GPRMC" \
            or items[2] != "A":
        return None

    gpsdatetime = datetime.datetime(year=2000 + int(items[9][4:6]),
                                    month=int(items[9][2:4]),
                                    day=int(items[9][0:2]),
                                    hour=int(items[1][0:2]),
                                    minute=int(items[1][2:4]),
                                    second=int(items[1][4:6]),
                                    microsecond=1000 * int(items[1][7:10]),
                                    tzinfo=pytz.UTC)

    return gpsdatetime
