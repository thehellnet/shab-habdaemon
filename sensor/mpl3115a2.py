import logging
from smbus import SMBus

bus = SMBus(1)


class MPL3115A2:
    ADDRESS = 0x60

    REGISTER_STATUS = 0x00
    REGISTER_STATUS_TDR = 0x02
    REGISTER_STATUS_PDR = 0x04
    REGISTER_STATUS_PTDR = 0x08

    REGISTER_PRESSURE_MSB = 0x01
    REGISTER_PRESSURE_CSB = 0x02
    REGISTER_PRESSURE_LSB = 0x03

    REGISTER_TEMP_MSB = 0x04
    REGISTER_TEMP_LSB = 0x05

    REGISTER_DR_STATUS = 0x06

    OUT_P_DELTA_MSB = 0x07
    OUT_P_DELTA_CSB = 0x08
    OUT_P_DELTA_LSB = 0x09

    OUT_T_DELTA_MSB = 0x0A
    OUT_T_DELTA_LSB = 0x0B

    BAR_IN_MSB = 0x14

    WHOAMI = 0x0C

    PT_DATA_CFG = 0x13
    PT_DATA_CFG_TDEFE = 0x01
    PT_DATA_CFG_PDEFE = 0x02
    PT_DATA_CFG_DREM = 0x04

    CTRL_REG1 = 0x26
    CTRL_REG1_SBYB = 0x01
    CTRL_REG1_OST = 0x02
    CTRL_REG1_RST = 0x04
    CTRL_REG1_OS1 = 0x00
    CTRL_REG1_OS2 = 0x08
    CTRL_REG1_OS4 = 0x10
    CTRL_REG1_OS8 = 0x18
    CTRL_REG1_OS16 = 0x20
    CTRL_REG1_OS32 = 0x28
    CTRL_REG1_OS64 = 0x30
    CTRL_REG1_OS128 = 0x38
    CTRL_REG1_RAW = 0x40
    CTRL_REG1_ALT = 0x80
    CTRL_REG1_BAR = 0x00
    CTRL_REG2 = 0x27
    CTRL_REG3 = 0x28
    CTRL_REG4 = 0x29
    CTRL_REG5 = 0x2A

    REGISTER_STARTCONVERSION = 0x12

    logger = logging.getLogger("MPL3115A2")

    def __init__(self, smbus):
        self._smbus = smbus
        self._initialized = False

    def init(self):
        self.logger.debug("Initialization")
        # self.logger.debug("Querying MPL3115A2 in I2C bus")
        # response = bus.read_byte_data(MPL3115A2.ADDRESS, MPL3115A2.WHOAMI)
        # if response != 0xc4:
        #     self.logger.error("MPL3115A2 device not active")
        #     return

        bus.write_byte_data(MPL3115A2.ADDRESS,
                            MPL3115A2.CTRL_REG1,
                            MPL3115A2.CTRL_REG1_SBYB | MPL3115A2.CTRL_REG1_OS128 | MPL3115A2.CTRL_REG1_ALT)

        bus.write_byte_data(MPL3115A2.ADDRESS,
                            MPL3115A2.PT_DATA_CFG,
                            MPL3115A2.PT_DATA_CFG_TDEFE | MPL3115A2.PT_DATA_CFG_PDEFE | MPL3115A2.PT_DATA_CFG_DREM)

        self.logger.debug("Initialization completed")
        self._initialized = True

    def poll(self):
        self.logger.debug("Polling")

        if not self._initialized:
            self.logger.warn("Sensor not initialized")
            return

        sta = 0
        while not (sta & MPL3115A2.REGISTER_STATUS_PDR):
            sta = bus.read_byte_data(MPL3115A2.ADDRESS, MPL3115A2.REGISTER_STATUS)

        self.logger.debug("Polling completed")

    def altitude(self):
        self.logger.debug("Reading altitude")

        if not self._initialized:
            self.logger.warn("Sensor not initialized")
            return

        bus.write_byte_data(MPL3115A2.ADDRESS,
                            MPL3115A2.CTRL_REG1,
                            MPL3115A2.CTRL_REG1_SBYB | MPL3115A2.CTRL_REG1_OS128 | MPL3115A2.CTRL_REG1_ALT)
        self.poll()

        msb, csb, lsb = bus.read_i2c_block_data(MPL3115A2.ADDRESS, MPL3115A2.REGISTER_PRESSURE_MSB, 3)
        alt = ((msb << 24) | (csb << 16) | (lsb << 8)) / 65536.
        if alt > (1 << 15):
            alt -= 1 << 16

        return alt

    def temperature(self):
        self.logger.debug("Reading temperature")

        if not self._initialized:
            self.logger.warn("Sensor not initialized")
            return

        bus.write_byte_data(MPL3115A2.ADDRESS,
                            MPL3115A2.CTRL_REG1,
                            MPL3115A2.CTRL_REG1_SBYB | MPL3115A2.CTRL_REG1_OS128 | MPL3115A2.CTRL_REG1_ALT)
        self.poll()

        msb, lsb = bus.read_i2c_block_data(MPL3115A2.ADDRESS, MPL3115A2.REGISTER_TEMP_MSB, 2)
        return (((msb << 8) | lsb) >> 4) * 0.0625

    def pressure(self):
        self.logger.debug("Reading pressure")

        if not self._initialized:
            self.logger.warn("Sensor not initialized")
            return

        bus.write_byte_data(MPL3115A2.ADDRESS,
                            MPL3115A2.CTRL_REG1,
                            MPL3115A2.CTRL_REG1_SBYB | MPL3115A2.CTRL_REG1_OS128 | MPL3115A2.CTRL_REG1_BAR)
        self.poll()

        msb, csb, lsb = bus.read_i2c_block_data(MPL3115A2.ADDRESS, MPL3115A2.REGISTER_PRESSURE_MSB, 3)
        return ((msb << 16) | (csb << 8) | lsb) / 64.

    def calibrate(self):
        self.logger.debug("Calibrating")

        if not self._initialized:
            self.logger.warn("Sensor not initialized")
            return

        pa = int(self.pressure() / 2)
        bus.write_i2c_block_data(MPL3115A2.ADDRESS, MPL3115A2.BAR_IN_MSB, [pa >> 8 & 0xff, pa & 0xff])
