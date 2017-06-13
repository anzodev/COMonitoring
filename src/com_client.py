#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import time
from sys import platform
from glob import glob
from threading import Thread
import socket
import serial
import os


# functions
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('google.co.uk', 80))
        return s.getsockname()[0]
    except:
        return '127.0.0.1'


def socket_send_to(host, port, str_data):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send(str.encode(str_data))
    s.close()


def time_convert(millis):
    millis  = int(millis)
    seconds = int((millis / 1000) % 60)
    minutes = int((millis / (1000 * 60)) % 60)
    hours   = int((millis / (1000 * 60 * 60)) % 24)
    days    = int((millis / (1000 * 60 * 60 * 24) % 24))

    if days >= 1:
        return '%sd' % days
    else:
        return time(hour = hours, minute = minutes, second = seconds).isoformat()


def signal_level_value(package):
    start_point = package.find('[')
    end_point   = package.find(']')
    package     = package[start_point+2:end_point-1].replace(' ', ',')
    return package


def create_package(package):
    values  = signal_level_value(package)
    package = package.split(' ')
    serial  = package[0].strip('\r\n\n')
    number  = package[1][1:-1]
    time    = int(package[2], 16)
    package = { "serial"  : serial,
                            "number"  : number,
                            "time"    : time_convert(str(time)),
                            "values"  : values }
    return package


def serial_ports():
    if platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif platform.startswith('linux') or platform.startswith('cygwin'):
        ports = glob('/dev/tty[A-Za-z]*')
    elif platform.startswith('darwin'):
        ports = glob('/dev/tty.*')
    else:
        raise EnvironmentError('unsupported platform...')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


def listen_client_command():
    s_command = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_command.bind((get_ip(), 12000))
    s_command.listen(1)

    global client_command

    while True:
        try:
            connect, address = s_command.accept()
            data             = connect.recv(1024)
            client_command   = bytes.decode(data)
            connect.close()
        except:
            pass


# script start
if __name__ == '__main__':

    # global variables
    server_ip           = ''
    server_port_send    = 10000
    server_port_connect = 8000
    client_ip           = get_ip()
    base_ip             = client_ip[:client_ip.rfind('.') + 1]

    client_command      = ''
    disconnect_toggle   = True

    t = Thread(target = listen_client_command, args = ())
    t.daemon = True
    t.start()

    # identify server ip address
    for i in range(256):
        check_ip = base_ip + str(i)
        try:
            check_connection = socket.create_connection((check_ip, server_port_send), 0.01)
            check_connection.close()
            server_ip = check_ip
            break
        except:
            pass

    # open default browser with right page
    print('connect to %s successful...' % server_ip)
    os.system("start \"\" http:" + server_ip + ":" + str(server_port_connect))


    while True:

        # detect client's pause
        if client_command == 'pause':
            try:
                socket_send_to(server_ip,
                               server_port_send,
                               str({'pause': client_ip.replace("'",'"')}))
            except:
                pass

            while client_command != 'work':
                pass

        elif client_command == 'work':
            try:
                socket_send_to(server_ip,
                               server_port_send,
                               str({'work': client_ip.replace("'",'"')}))
            except:
                pass

            client_command = ''

        else:
            # identify avaliable COM ports
            connected_ports = serial_ports()
            package         = {}

            if connected_ports == []:
                if disconnect_toggle:
                    try:
                        socket_send_to(server_ip,
                                       server_port_send,
                                       str({'disconnect': client_ip.replace("'",'"')}))
                        disconnect_toggle = False
                    except:
                        pass
            else:
                for port in connected_ports:
                    # port initialization
                    ser          = serial.Serial()
                    ser.port     = port
                    ser.baudrate = 9600
                    ser.timeout  = None
                    ser.bytesize = serial.EIGHTBITS
                    ser.stopbits = serial.STOPBITS_ONE
                    ser.parity   = serial.PARITY_NONE
                    ser.xonxoff  = False
                    ser.rtscts   = False
                    ser.dsrdtr   = False

                    # getting data from port
                    try:
                        ser.open()
                        port_data = ser.readline().decode('utf-8')
                        ser.close()
                    except:
                        pass

                    # create new element for global package
                    package[port] = create_package(port_data)

                # sending global package
                try:
                    socket_send_to(server_ip,
                                   server_port_send,
                                   str({client_ip: package}).replace("'",'"'))
                except:
                    pass

                disconnect_toggle = True