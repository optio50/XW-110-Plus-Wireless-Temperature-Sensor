A simple PYQT5 interface with a 7 day live chart and current readout for the XW-110 wireless temperature sensors.    
Uses ModBusTCP for communication with the sensors.
Chart and readout are updated every 5 seconds. Chart will hold 7 days of data.    
It has no ability to hold values after closing. Data is held only when running.   
Tested with pymodbus 3.6.3


https://www.controlbyweb.com/xw110/    
The XW-110 is an easy-to-use wireless temperature sensor with a built-in web server.    
Users can view current temperature using a web browser, smartphone app,    
or the XW-110 can send temperature information via email.    
The XW-110 can be easily and quickly mounted to a wall or any other workable surface. 

![ScreenShot](https://raw.githubusercontent.com/optio50/XW-110-Plus-Wireless-Temperature-Sensor/main/ModBus-PYQT5-XW-110P.png?raw=true|alt=octocat)    
![ScreenShot](https://raw.githubusercontent.com/optio50/XW-110-Plus-Wireless-Temperature-Sensor/main/Modbus-XW-110P-CLI.png?raw=true|alt=octocat)    
![ScreenShot](https://raw.githubusercontent.com/optio50/XW-110-Plus-Wireless-Temperature-Sensor/main/xw110-external-temp-sensor.jpg?raw=true|alt=octocat)

to install    
`pip install pymodbus`    
`pip install pglive`    
for the PYQT5 file you need to have PYQT5 installed. Try with your distro packagemanager    
such as `sudo apt install python3-pyqt5`    
When using the PYQT5 files you only need to run the python file. The .ui will load automatically.    
You can also edit the .ui file with QT designer which is part of PYQT5

The CLI py file is just a simple python example how modbus works with the WebRelay devices.    
Running it will simply display the Temperatures on the screeen a single time.
