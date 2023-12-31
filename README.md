![ScreenShot](https://raw.githubusercontent.com/optio50/XW-110-Plus-Wireless-Temperature-Sensor/main/ModBus-PYQT5-XW-110P.png?raw=true|alt=octocat)    
![ScreenShot](https://raw.githubusercontent.com/optio50/XW-110-Plus-Wireless-Temperature-Sensor/main/Modbus-XW-110P-CLI.png?raw=true|alt=octocat)    


to install    
`pip install pymodbus`    
`pip install pglive`    
for the PYQT5 file you need to have PYQT5 installed. Try with your distro packagemanager    
such as `sudo apt install python3-pyqt5`    
When using the PYQT5 files you only need to run the python file. The .ui will load automatically.    
You can also edit the .ui file with QT designer which is part of PYQT5

The CLI py file is just a simple python example how modbus works with the WebRelay devices.    
Running it will simply display the Temperatures on the screeen a single time.
