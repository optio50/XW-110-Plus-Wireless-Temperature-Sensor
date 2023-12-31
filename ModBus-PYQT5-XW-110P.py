#!/usr/bin/python3
import signal
from threading import Thread

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTime, QTimer, QProcess, Qt, QObject, QThread
from PyQt5 import uic, QtGui
from PyQt5.QtGui import QColor, QIcon

from time import sleep
import time
from datetime import datetime

# Chart
import pyqtgraph as pg
from pyqtgraph import mkPen
from pglive.kwargs import Axis, Crosshair, LeadingLine
from pglive.sources.data_connector import DataConnector
from pglive.sources.live_axis import LiveAxis
from pglive.sources.live_plot import LiveLinePlot
from pglive.sources.live_axis_range import LiveAxisRange
from pglive.sources.live_plot_widget import LivePlotWidget

# Modbus
from pymodbus.constants import Defaults
from pymodbus.constants import Endian
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder

# IP Address of XW-110P
ip = '192.168.20.2'
client = ModbusClient(ip, port='502')

'''
Right Click drag (left right up down) to zoom in and out for the axis of choice
Mouse wheel zooms in / out.
Right Click "View All"
Click the lower left corner "A" to auto scale after zooming or panning.
'''

def modbus_register(address, units):
    msg     = client.read_holding_registers(address, units)
    decoder = BinaryPayloadDecoder.fromRegisters(msg.registers, Endian.Big)
    msg     = decoder.decode_32bit_float()
    return msg


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Load the ui file
        uic.loadUi("ModBus-PYQT5-XW-110P.ui", self)
        icon = QIcon("skin.png")
        self.setWindowIcon(QtGui.QIcon(icon))

        Started = datetime.now()
        # Fri 21 Jan 2022     09:06:57 PM
        dt_string = Started.strftime("%a %d %b %Y     %r")
        self.Start_Label.setText("App Started on " + dt_string)

#===========================================================================================
# Begin Chart
        kwargs = {Crosshair.ENABLED: True,
        Crosshair.LINE_PEN: pg.mkPen(color="yellow", width=.5),
        Crosshair.TEXT_KWARGS: {"color": "darkorange"}}
        pg.setConfigOption('background', "black")

        # Chart Solar Volts
        Sensor1_plot  = LiveLinePlot(pen="red",   name="Sensor1")
        Sensor2_plot  = LiveLinePlot(pen="blue",  name="Sensor2")
        Sensor3_plot  = LiveLinePlot(pen="green", name="Sensor3")

        # Data connectors for each plot with dequeue of max_points points
        self.Sensor1_connector = DataConnector(Sensor1_plot, max_points=86400, update_rate=.4)
        self.Sensor2_connector = DataConnector(Sensor2_plot, max_points=86400, update_rate=.4)
        self.Sensor3_connector = DataConnector(Sensor3_plot, max_points=86400, update_rate=.4)

        # Setup bottom axis with TIME tick format
        # use Axis.DATETIME to show date
        bottom_axis = LiveAxis("bottom", **{Axis.TICK_FORMAT: Axis.DATETIME})


        # Create plot itself
        self.Temperature_graph_Widget = LivePlotWidget(title="XW-110 Plus Wireless Temperature Sensor 7 Day Chart",
                                      axisItems={'bottom': bottom_axis},
                                      x_range_controller=LiveAxisRange(roll_on_tick=300, offset_left=.5), **kwargs)

        self.Temperature_graph_Widget.x_range_controller.crop_left_offset_to_data = True


        # Show grid
        self.Temperature_graph_Widget.showGrid(x=True, y=True, alpha=0.3)


        # Set labels
        self.Temperature_graph_Widget.setAxisItems(axisItems={'bottom': bottom_axis})
        self.Temperature_graph_Widget.setLabels(left='Deg F')

        self.Temperature_graph_Widget.addLegend()

        # Add Line
        self.Temperature_graph_Widget.addItem(Sensor1_plot)
        self.Temperature_graph_Widget.addItem(Sensor2_plot)
        self.Temperature_graph_Widget.addItem(Sensor3_plot)


        # Add chart to Layout in Qt Designer
        self.Temperature_layout.addWidget(self.Temperature_graph_Widget)
# End Chart
#===========================================================================================
# Make QTimer for Clock Display
        self.qTimer1 = QTimer()

        # set interval to 1 s.
        self.qTimer1.setInterval(1000) # 1000 ms = 1 s

        # connect timeout signal to signal handler
        self.qTimer1.timeout.connect(self.showTime)

        # start timer
        self.qTimer1.start()
#===========================================================================================
# Make QTimer for UI update
        self.qTimer3 = QTimer()

        # set interval to 1 s.
        self.qTimer3.setInterval(5000) # 1000 ms = 1 s

        # connect timeout signal to signal handler
        self.qTimer3.timeout.connect(self.update_ui)

        # start timer
        self.qTimer3.start()
#===========================================================================================
# Make QTimer for Chart update
        self.qTimer4 = QTimer()

        # set interval to 1 s.
        self.qTimer4.setInterval(5000) # 1000 ms = 1 s

        # connect timeout signal to signal handler
        self.qTimer4.timeout.connect(self.update_charts)

        # start timer
        self.qTimer4.start()
#===========================================================================================

    def update_ui(self): # Update all the UI widgets
        #print("udate ui ran")
        global Sensor1, Sensor2, Sensor3
        Sensor1 = modbus_register(272, 2)
        Sensor2 = modbus_register(274, 2)
        Sensor3 = modbus_register(276, 2)
        self.Sensor1_lcdNumber.display(float(Sensor1))
        self.Sensor2_lcdNumber.display(float(Sensor2))
        self.Sensor3_lcdNumber.display(float(Sensor3))


    def update_charts(self):
        try:
            global Sensor1, Sensor2, Sensor3
            timestamp = time.time() # for chart
            self.Sensor1_connector.cb_append_data_point(float(Sensor1), timestamp)
            self.Sensor2_connector.cb_append_data_point(float(Sensor2), timestamp)
            self.Sensor3_connector.cb_append_data_point(float(Sensor3), timestamp)
        except TypeError:
            pass


    def showTime(self):
        # Datetime object containing current date and time
        now = datetime.now()
        # Fri 21 Jan 2022     09:06:57 PM
        dt_string = now.strftime("%a %d %b %Y     %r")
        self.Time_Label.setText(dt_string)

app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())
