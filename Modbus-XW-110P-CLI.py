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

# Sensor display names
SENSOR1_NAME = "Sensor 1"
SENSOR2_NAME = "Sensor 2"
SENSOR3_NAME = "Sensor 3"

ip = '192.168.20.2'
client = ModbusClient(ip, port='502')

def modbus_register(address, slave):
    msg = client.read_holding_registers(address, count=2, device_id=slave)
    msg = struct.unpack(">f", struct.pack(">HH", *msg.registers))[0]
    return msg

print("\033[H\033[J")       # Clear screen once at startup
print('\033[?25l', end="")  # Hide blinking cursor
clear = "\033[K\033[1K"     # Eliminates screen flashing / blink during refresh

def arrow(current, previous):
    if previous is None:
        return " "
    if current > previous:
        return "↑"
    if current < previous:
        return "↓"
    return " "

prev1 = prev2 = prev3 = None

try:
    while True:
        print("\033[0;0f")  # Move cursor to row 0, col 0 (home)
        try:
            BatteryVoltage = modbus_register(16, 2)
            Sensor1        = modbus_register(272, 2)
            Sensor2        = modbus_register(274, 2)
            Sensor3        = modbus_register(276, 2)
            print(clear, f"  {Red}{SENSOR1_NAME} Temperature ......{Sensor1: .2f} °F {arrow(Sensor1, prev1)}{Reset}", sep="")
            print(clear, f"  {Blue}{SENSOR2_NAME} Temperature ......{Sensor2: .2f} °F {arrow(Sensor2, prev2)}{Reset}", sep="")
            print(clear, f"  {Green}{SENSOR3_NAME} Temperature ......{Sensor3: .2f} °F {arrow(Sensor3, prev3)}{Reset}", sep="")
            print(clear, f"  {DarkOrange}BatteryVoltage ...........{BatteryVoltage: .2f} Volts{Reset}", sep="")
            print(clear, f"  Last updated: {time.strftime('%a %d %b %Y  %I:%M:%S %p')}   (every {REFRESH_INTERVAL}s)", sep="")
            prev1, prev2, prev3 = Sensor1, Sensor2, Sensor3
        except Exception as e:
            print(clear, f"  Connection error: {e}", sep="")
        time.sleep(REFRESH_INTERVAL)
except KeyboardInterrupt:
    print('\033[?25h', end="")  # Restore cursor
    print("\033[H\033[J", end="")  # Clear screen
    print(Reset, end="")          # Reset colors
