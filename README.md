# COMonitoring

Monitoring system of signal level that use programmable modules Pololu Wixel and Python scripts.

> Current version stably works on Windows. The system can support up to 5 clients with 10 Wixels on each.  

## Requirements

1. Server and clients in one network.
2. [Python 3.6+](https://www.python.org/downloads/).
3. Modules flask and flask_socketio:
```
C:\pip install flask flask_socketio
```

## Hardware

Pololu Wixel

![Pololu Wixel](https://github.com/anzodev/COMonitoring/blob/master/pictures/wixels.png)

## Software

1. [Download](https://www.pololu.com/docs/0J46/3.a) and install Windows driver.
2. [Download](https://www.pololu.com/docs/0J46/10.a) Wixel SDK.
3. [Use](https://www.pololu.com/docs/0J46/10.b) this manual to load firmware.
4. Load the [firmware](wixel-sdk/apps/RPi_2oleds_ssd1306) into Pololu Wixel.

> For additional information see manufacturer [User's Guide](https://www.pololu.com/docs/0J46).

## How Does It Work

Wixel starts sending a data about signal level after its connection. Python client script finds all connected devices via virtual COM ports and gets data thrue them and sends to the server. The server sends this data to the client's browser.

![COMonitoring scheme](https://github.com/anzodev/COMonitoring/blob/master/pictures/comonitoring.jpg)

## Run
1. Put the [server part](https://github.com/anzodev/COMonitoring/tree/master/app/server) of system into the server's computer. Run **com_server.py**.
2. Run [client's script](https://github.com/anzodev/COMonitoring/tree/master/app/client) on client's computers. For Windows users there is the executable version **com_client.msi** so you dont need to install Python on your client's computer. Script open default browser with right page automatically.
3. Connect Wixel devices to client's computer.

> Server's and client's scripts can work from the one computer.

![Connecting Wixel devices](https://github.com/anzodev/COMonitoring/blob/master/pictures/wixel-connection.jpg)

## User's Web Interface

Web interface consists of two parts. On the left side is graph with signal level.

![Graph](https://github.com/anzodev/COMonitoring/blob/master/pictures/graph.jpg)

On the right side are details about connected clients and his devices.

![Client interface](https://github.com/anzodev/COMonitoring/blob/master/pictures/client-interface.jpg)
1. Client's name.
2. Pause button.
3. Client's ip and quantity of connected devices.
4. Port's name.
5. MAC.
6. Package number.
7. Device working time.

Also the interface has some functional:
1. You can set the client name if you need. Just tap on the name's area. This name is assigned to the client's ip on the server.

  ![Change name](https://github.com/anzodev/COMonitoring/blob/master/pictures/change-name.jpg)

2. To safely disconnect Wixel device from computer click on the pause button. Otherwise you can disconnect while receiving the data from Wixel and script stop working.

  ![Pause button](https://github.com/anzodev/COMonitoring/blob/master/pictures/pause.jpg)

3. You can hide the graph for each COM port. Tap on the port's name.

  ![Hide graph](https://github.com/anzodev/COMonitoring/blob/master/pictures/hide-graph.jpg)


## Task List
- [ ] To make client and server scripts executable for OS Windows, Linux, Mac OS.
- [ ] To add mobile version of system's web page.
- [ ] To create handler in the client's script when connection with server is lost. One of the client has to do server's work.
- [ ] To modify the system for supporting more than five client.
- [ ] Add the functional for creating network's signal level topology.


## Licenses

The source code are licensed under the [GNU GPLv3](https://www.gnu.org/licenses/gpl-3.0.html). The schematics are licensed under the [CC-BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/).

## Authors

Developer - Ivan Bogachuk  
Manager - Vladimir Sokolov



