"""
Created on 29 Dec 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_host.bus.i2c import I2C

from scs_psu.psu.opcube_v1.psu_status import ChargerStatus


# --------------------------------------------------------------------------------------------------------------------

class IOExpander(object):
    """
    Texas Instruments PCA9534A or NXP PCA9849 remote 8-bit I/O expander
    """

    __ADDR_INPUT =          0x00
    __ADDR_OUTPUT =         0x01
    __ADDR_INVERSION =      0x02
    __ADDR_CONFIG =         0x03

    __CONFIG =              0xcf        # 1100 1111

    __MASK_BAT_TOC =        0x01        # 0000 0001     (mislabeled as TOC on schematic)
    __MASK_BAT_READY =      0x02        # 0000 0010
    __MASK_BAT_FAULT =      0x04        # 0000 0100
    __MASK_BAT_CHARGE =     0x08        # 0000 1000

    __MASK_LED2 =           0x10        # 0001 0000
    __MASK_LED1 =           0x20        # 0010 0000


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, addr):
        """
        Constructor
        """
        self.__addr = int(addr)


    # ----------------------------------------------------------------------------------------------------------------

    def init(self):
        self.__configure(self.__CONFIG)
        self.__output(0x00)


    def set_leds(self, led1, led2):
        led1_mask = self.__MASK_LED1 if led1 else 0x00
        led2_mask = self.__MASK_LED2 if led2 else 0x00

        self.__output(led1_mask | led2_mask)


    def sample(self):
        state = self.__input()

        ready = bool(state & self.__MASK_BAT_READY)
        fault = not bool(state & self.__MASK_BAT_FAULT)
        charging = not bool(state & self.__MASK_BAT_CHARGE)
        power_fail = not bool(state & self.__MASK_BAT_TOC)

        return ChargerStatus(ready, fault, charging, power_fail)


    # ----------------------------------------------------------------------------------------------------------------

    def __configure(self, configuration):
        try:
            I2C.Utilities.start_tx(self.__addr)
            I2C.Utilities.write_addr(self.__ADDR_CONFIG, configuration)

        finally:
            I2C.Utilities.end_tx()


    def __input(self):
        try:
            I2C.Utilities.start_tx(self.__addr)
            return I2C.Utilities.read_cmd(self.__ADDR_INPUT, 1)

        finally:
            I2C.Utilities.end_tx()


    def __output(self, byte):
        try:
            I2C.Utilities.start_tx(self.__addr)
            I2C.Utilities.write_addr(self.__ADDR_OUTPUT, byte)

        finally:
            I2C.Utilities.end_tx()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return self.__class__.__name__ + ":{addr:0x%02x}" % self.__addr


# --------------------------------------------------------------------------------------------------------------------

class PCA9534A(IOExpander):
    """
    Texas Instruments PCA9534A remote 8-bit I/O expander
    """

    DEFAULT_ADDR =              0x38                # I2C address

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor
        """
        super().__init__(self.DEFAULT_ADDR)


# --------------------------------------------------------------------------------------------------------------------

class PCA9849(IOExpander):
    """
    NXP PCA9849 remote 8-bit I/O expander
    """

    DEFAULT_ADDR =              0x20                # I2C address

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor
        """
        super().__init__(self.DEFAULT_ADDR)



