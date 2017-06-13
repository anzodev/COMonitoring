# COMonitoring

Monitoring system of signal level that uses programmable modules Pololu Wixel and [Python 3.6+](https://www.python.org/downloads/).

> Current version was created for OS Windows. You can run it on another OS using Python scripts in [src](/src) folder and module [cx_Freeze](http://cx-freeze.readthedocs.io/en/latest/index.html). The system supports up to 5 clients with 10 Wixels on each.    

## Hardware

Pololu Wixel

![Pololu Wixel](https://github.com/anzodev/COMonitoring/blob/master/pict/wixels.png)

## Software

1. [Download](https://www.pololu.com/docs/0J46/3.a) and install Windows driver.
2. [Download](https://www.pololu.com/docs/0J46/10.a) Wixel SDK.
3. [Use](https://www.pololu.com/docs/0J46/10.b) this manual to load firmware.
4. Load the [firmware](wixel-sdk/apps/RPi_2oleds_ssd1306) into Pololu Wixel.

> For additional information see manufacturer [User's Guide](https://www.pololu.com/docs/0J46).

## How Does It Work

Wixel starts sending a data about signal level after its connection. Python client's app finds all connected devices via virtual COM ports and gets data thrue them and sends to the server. The server sends this data to the client's browser.

## Run
1. Put the [server part](https://github.com/anzodev/COMonitoring/tree/master/app) of the system into the server's computer. Run **com_server.exe**.
2. Put the [client part](https://github.com/anzodev/COMonitoring/tree/master/app) of the system into the clients' computers. Run **com_client.exe**. The app opens default browser with right page.
> Client's app can works with server's app from the one computer.
3. Connect Wixel devices to client's computer.

![Connecting Wixel devices](https://github.com/anzodev/COMonitoring/blob/master/pict/connecting-devices.png)

## User's Web Interface

Web interface consists of two parts. On the left side there is graph with data of signal level from Wixels.

![Graph](https://github.com/anzodev/COMonitoring/blob/master/pict/graph.png)

On the right side there are details about connected clients and their devices.

![Client interface](https://github.com/anzodev/COMonitoring/blob/master/pict/ui.png)
___

The interface has functional:
1. To set the client's name click on the name's area. After changing this name is assigned to the client's ip on the server for saving.

&emsp;![Change name](https://github.com/anzodev/COMonitoring/blob/master/pict/click-name.png)

2. To safely disconnect Wixel device from computer click on the pause button. Otherwise, when you disconnect while receiving the data from Wixel the client's app stops working. 

&emsp;![Pause button](https://github.com/anzodev/COMonitoring/blob/master/pict/click-pause.png)

3. You can hide the graph for each COM port. Click on the port's name. 

&emsp;![Hide graph](https://github.com/anzodev/COMonitoring/blob/master/pict/click-port.png)


## Task List
- [ ] To make client and server scripts executable for Linux, Mac OS.
- [ ] To add mobile version of system's web page.
- [ ] To create handler in the client's script when connection with server is lost. One of the client has to perform server's role.
- [ ] To modify the system for supporting more than five clients.
- [ ] Add the functional for creating network's signal level topology.


## Licenses

The source code are licensed under the [GNU GPLv3](https://www.gnu.org/licenses/gpl-3.0.html). The schematics are licensed under the [CC-BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/).

## Authors

Developer - Ivan Bogachuk  
Manager - Vladimir Sokolov



