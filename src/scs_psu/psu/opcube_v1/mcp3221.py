"""
Created on 29 Dec 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.datum import Decode

from scs_host.bus.i2c import I2C


# --------------------------------------------------------------------------------------------------------------------

class MCP3221(object):
    """
    Microchip MCP3221A 12-bit ADC
    """

    DEFAULT_ADDR =      0x48

    __VDD =             3.3             # Volts
    __RANGE =           4095            # count
    __DIVISION =        11              # voltage divider is 10:1

    __LSB =             __VDD / __RANGE
    __CONV =            __LSB * __DIVISION

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, addr):
        """
        Constructor
        """
        self.__addr = int(addr)


    # ----------------------------------------------------------------------------------------------------------------

    def sample(self):
        byte_values = self.__convert()
        code = Decode.unsigned_int(byte_values, '>')
        v = code * self.__CONV

        return round(v, 1)


    # ----------------------------------------------------------------------------------------------------------------

    def __convert(self):
        try:
            I2C.Utilities.start_tx(self.__addr)
            return I2C.Utilities.read(2)

        finally:
            I2C.Utilities.end_tx()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MCP3221:{addr:0x%02x}" % self.__addr
