#!/usr/bin/python3
# -*- coding: utf-8 -*-

from sys import platform
from glob import glob
from threading import Thread
import socket
import serial
import os


def get_ip():
    '''Get the network adapter's IP address.'''
    return socket.gethostbyname_ex(socket.gethostname())[2][0]


def socket_send_to(host, port, data):
    '''Send data to some host using TCP.

    Keyword arguments:
    host -- hostname for connection
    port -- port number for connection
    data -- data that is transmitted
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send(str.encode(str_data))
    s.close()


def time_convert(ms):
    '''Convert time from milliseconds to string like "11:06:34".

    Keyword arguments:
    ms -- milliseconds
    '''
    s = (int(ms) // 1000) % 60
    m = (int(ms) // 60000) % 60
    h = (int(ms) // 3600000) % 24
    return '%02d:%02d:%02d' % (h, m, s)


def signal_level_value(package):
    '''Slice signal's values from the package.

    Keyword arguments:
    package -- received package with data
    '''
    start_point = package.find('[')
    end_point   = package.find(']')
    return package[start_point + 2:end_point - 1].replace(' ', ',')


def create_package(package):
    '''Form new package with structured data using received package.

    Keyword arguments:
    package -- received package with data
    '''
    values  = signal_level_value(package)
    package = package.split(' ')
    serial  = package[0].strip('\r\n\n')
    number  = package[1][1:-1]
    time    = int(package[2], 16)
    package = {"serial": serial, "number": number,
               "time": time_convert(str(time)), "values": values}
    return package


def serial_ports():
    '''Check available COM connections.'''
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
    '''Listen commands from browsers.'''
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


if __name__ == '__main__':
    server_ip           = ''
    server_port_send    = 10000
    server_port_connect = 8000
    client_ip           = get_ip()
    base_ip             = client_ip[:client_ip.rfind('.') + 1]
    client_command      = ''
    disconnect_toggle   = True

    # starting new process with listening command from client
    t = Thread(target = listen_client_command, args = ())
    t.daemon = True
    t.start()

    # trying to find server IP address by creation connection to the server.
    for i in range(256):
        check_ip = base_ip + str(i)
        try:
            check_connection = socket.create_connection((check_ip, server_port_send), 0.01)
            check_connection.close()
            server_ip = check_ip
            break
        except:
            pass

    # if the loop above doesn't find any ip address, client have to input it
    if server_ip == '':
        server_ip = input('input server IP address: ')

    # run browser with connection to server
    os.system("start \"\" http:" + server_ip + ":" + str(server_port_connect))

    while True:

        if client_command == 'pause':
            try:
                socket_send_to(server_ip, server_port_send,
                               str({'pause': client_ip.replace('\'','"')}))
            except:
                pass

            while client_command != 'work':
                pass

        elif client_command == 'work':
            try:
                socket_send_to(server_ip, server_port_send,
                               str({'work': client_ip.replace('\'','"')}))
            except:
                pass

            client_command = ''

        else:
            connected_ports = serial_ports()
            package         = {}

            if connected_ports != []:
                for port in connected_ports:
                    # serialize COM port
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

                    try:
                        ser.open()
                        port_data = ser.readline().decode('utf-8')
                        ser.close()
                    except:
                        pass

                    package[port] = create_package(port_data)

                try:
                    socket_send_to(server_ip, server_port_send,
                                   str({client_ip: package}).replace('\'','"'))
                except:
                    pass

                disconnect_toggle = True
            else:
                if disconnect_toggle:
                    try:
                        socket_send_to(server_ip, server_port_send,
                                       str({'disconnect': client_ip.replace('\'','"')}))
                        disconnect_toggle = False
                    except:
                        pass