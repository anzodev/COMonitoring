#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from engineio import async_threading
from time import sleep
import socket


def get_ip():
    '''Get the network adapter's IP address.'''
    return socket.gethostbyname_ex(socket.gethostname())[2][0]


def get_send_data():
    '''Receive package and send it to client's browser.'''
    s_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_server.bind((get_ip(), 10000))
    s_server.listen(5)

    global client_name

    while True:
        try:
            connect, address = s_server.accept()
            data = connect.recv(16384)
            data = bytes.decode(data)

            if data[2:7] == "pause" or data[2:6] == "work":
                socketio.emit('client_pause', {'data': data})
            elif data[2:12] == "disconnect":
                socketio.emit('client_disconnect', {'data': data})
            else:
                socketio.emit('get_show_data', {'data': data})

            connect.close()
        except:
            pass


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
socketio = SocketIO(app, async_mode="threading")


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect')
def connect():
    '''Client connection handler'''
    print('\nnew connection: ' + str(request.remote_addr) + '\n')

    global client_name
    sleep(1)
    socketio.emit('client_name', {'data': client_name})


@socketio.on('get_send_command')
def get_command(command):
    '''Send command from browser to the client's script'''
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((str(command[0]), 12000))
        s.send(str.encode(str(command[1])))
        s.close()
    except:
        pass


@socketio.on('get_client_name')
def get_client_name(name):
    '''Receive name from browser and save it in global dict.'''
    global client_name
    client_name[name[0]] = name[1]


if __name__ == '__main__':
    client_name = {}

    socketio.start_background_task(target = get_send_data)
    socketio.run(app, host = get_ip(), port = 8000)