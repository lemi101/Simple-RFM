import os
import select
import socket
import struct

def sort(op, params):
    if op.lower() == 'new':
        return new(params)
    elif op.lower() == 'read':
        return read(params)
    elif op.lower() == 'del':
        return delete(params)
    else:
        return 'Error, command not found...'

def new(file_name):
    try:
        f = open(file_name, 'x')
        f.close()
        return 'OK'
    except IOError:
        return 'Error, fail to create ' + file_name

def read(file_name):
    try:
        f = open(file_name, 'r')
        content = f.read()
        f.close()
        return content
    except IOError:
        return 'Error, fail to read ' + file_name

def delete(file_name):
    try:
        os.remove(file_name)
        return 'OK'
    except OSError:
        return 'Error, fail to delete ' + file_name

tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

tcp_sock.bind(('0.0.0.0', 1337))

tcp_sock.listen(10)

list_monitor = [tcp_sock]

print('Server Ready...')

while True:
    inready, outready, errready = select.select(list_monitor, [ ], [ ])

    for conn in inready:

        if conn == tcp_sock:
            conn, client_addr = tcp_sock.accept()
            list_monitor.append(conn)
        else:
            try:
                raw_data_len = conn.recv(4)
                data_len = struct.unpack('>I', raw_data_len)[0]

                data = b''

                while len(data) < data_len:
                    packet = conn.recv(data_len - len(data))
                    data += packet

                data = data.decode('ascii')
                data = str(data).split('|')
                data = sort(data[0], data[1])
                data = data.encode('ascii')
                data = struct.pack('>I', len(data)) + data

                conn.send(data)
            except struct.error:
                conn.close()
                list_monitor.remove(conn)

                print('Connection Closed by Client')
