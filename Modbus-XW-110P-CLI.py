#!/usr/bin/env python3
import struct
import time
# Modbus
from pymodbus.client import ModbusTcpClient as ModbusClient
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

REFRESH_INTERVAL = 5  # seconds between updates

ip = '192.168.20.2'
client = ModbusClient(ip, port='502')

def modbus_register(address, slave):
    msg = client.read_holding_registers(address, count=2, device_id=slave)
    msg = struct.unpack(">f", struct.pack(">HH", *msg.registers))[0]
    return msg

# Lines printed per cycle — must match exactly for flicker-free cursor repositioning
OUTPUT_LINES = 6

def print_readings():
    try:
        BatteryVoltage = modbus_register(16, 2)
        Sensor1        = modbus_register(272, 2)
        Sensor2        = modbus_register(274, 2)
        Sensor3        = modbus_register(276, 2)
        print(f"  {Red}Sensor1 Temperature ......{Sensor1: .2f} °F{Reset}     ")
        print(f"  {Blue}Sensor2 Temperature ......{Sensor2: .2f} °F{Reset}     ")
        print(f"  {Green}Sensor3 Temperature ......{Sensor3: .2f} °F{Reset}     ")
        print(f"  {DarkOrange}BatteryVoltage ...........{BatteryVoltage: .2f} Volts{Reset}  ")
        print(f"  Last updated: {time.strftime('%a %d %b %Y  %I:%M:%S %p')}   (every {REFRESH_INTERVAL}s)")
        print()
    except Exception as e:
        print(f"  Connection error: {e}                    ")
        print()
        print()
        print()
        print()
        print()

print()  # top spacer — printed once, never overwritten
first = True
while True:
    if not first:
        # Move cursor up OUTPUT_LINES lines and overwrite in place — no flicker
        print(f"\033[{OUTPUT_LINES}A", end="", flush=True)
    print_readings()
    first = False
    time.sleep(REFRESH_INTERVAL)
