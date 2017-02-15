#!/usr/bin/env python3

"""
Created on 9 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import serial


# --------------------------------------------------------------------------------------------------------------------

CMD_READ = 0x52
CMD_WRITE = 0x57
U = 0x55

ADDR_CHECK_VALUE = 0x00
ADDR_VERSION = 0x1f
ADDR_CMD_STATUS = 0x20
ADDR_PSU_STATUS = 0x21

POWER_CYCLE_ON = 0x01
COMMAND_CLEAR = 0x00


COMMAND_CONTROL = 0x07
POWER_CYCLE_WAIT_Mins = 0x01
POWER_CYCLE_WAIT_Secs = 0x02
POWER_CYCLE_DOWN_Mins = 0x03
POWER_CYCLE_DOWN_Secs = 0x04

BatteryV_LSB = 0x10
BatteryV_MSB = 0x11
SocketV_LSB = 0x12
SocketV_MSB = 0x13

uP_InternalStatus = 0x20

ser = serial.Serial('/dev/ttyO5', 115200)
ser.flush()

packet = bytearray([CMD_WRITE, POWER_CYCLE_WAIT_Secs, 0x20])
ser.write(packet)

packet = bytearray([CMD_READ, POWER_CYCLE_WAIT_Secs])
ser.write(packet)
chars = ser.read(1)
result = int(chars[0])

print("result:0x%02x" % result)


packet = bytearray([CMD_WRITE, POWER_CYCLE_DOWN_Secs, 0x05])
ser.write(packet)

packet = bytearray([CMD_READ, POWER_CYCLE_DOWN_Secs])
ser.write(packet)
chars = ser.read(1)
result = int(chars[0])

print("result:0x%02x" % result)


packet = bytearray([CMD_WRITE, COMMAND_CONTROL, COMMAND_CLEAR])
ser.write(packet)

packet = bytearray([CMD_WRITE, COMMAND_CONTROL, POWER_CYCLE_ON])
ser.write(packet)

print("Done")

ser.flush()

ser.close()
