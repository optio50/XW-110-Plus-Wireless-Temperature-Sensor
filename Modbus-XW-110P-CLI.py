#!/usr/bin/env python3
# Modbus
from pymodbus.constants import Endian
from pymodbus.client import ModbusTcpClient as ModbusClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
# XW-110 Plus Webrelay Wireless Temperature Monitoring System
# https://www.controlbyweb.com/xw110/
'''
To set up: pip install pymodbus

In Modbus communication, registers store 16-bit data.
The value 2 indicates that the code attempts to read two registers
starting from the register address.
Since the temperature data might be stored across multiple registers
(e.g., two consecutive registers to represent a 32-bit floating-point value),
the 2 specifies that the program expects to read two consecutive 16-bit
registers and then decode them accordingly.
'''
# Screen Formatting
# ANSI Color Codes
Red        = '\033[38;5;196m'
Blue       = '\033[38;5;21m'
Green      = '\033[38;5;34m'
DarkOrange = '\033[38;5;208m'
Reset      = '\033[0m'
Spacer     = "\n" * 10

ip = '192.168.20.2'
client = ModbusClient(ip, port='502')

def modbus_register(address, units):
    msg     = client.read_holding_registers(address, units)
    decoder = BinaryPayloadDecoder.fromRegisters(msg.registers, Endian.BIG)
    msg     = decoder.decode_32bit_float()
    return msg


BatteryVoltage = modbus_register(16, 2)
Sensor1        = modbus_register(272, 2)
Sensor2        = modbus_register(274, 2)
Sensor3        = modbus_register(276, 2)
print(Spacer)
print(f"{Red}  Sensor1 Temperature ......{Sensor1: .2f} °F{Reset}")
print(f"{Blue}  Sensor2 Temperature ......{Sensor2: .2f} °F{Reset}")
print(f"{Green}  Sensor3 Temperature ......{Sensor3: .2f} °F{Reset}")
print(f"{DarkOrange}  BatteryVoltage ...........{BatteryVoltage} Volts{Reset}")
print(Spacer)
