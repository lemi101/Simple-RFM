import socket
import struct

def help():
    print('Command List : ')
    print('new [filename] - add a new file - ex : new hello.txt')
    print('read [filename] - read a file - ex : read hello.txt')
    print('del [filename] - delete a file - ex : del hello.txt')
    print('help - print commmand list - ex : help')
    print('quit - end current season - ex : quit')


ip_addr = '127.0.0.1'
port = 1337

print('--------------------------------------------------------------')
print('---------------- [ Remote File Modification ] ----------------')
print('--------------------------------------------------------------')

tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

tcp_sock.connect((ip_addr, port))

print('IP Address : ' + ip_addr)
print('Connected on port : ' + str(port))
print('Type \'help\' for command list... ')

cond = True

while cond:
    data = input('> ')
    
    if data.lower() == 'help':
        help()
        break
    elif data.lower() == 'quit':
        cond = False
        tcp_sock.close()
        break
    else:
        data = str(data).replace(' ', '|')
        data = data.encode('ascii')
        data = struct.pack('>I', len(data)) + data
        tcp_sock.send(data)
        
        raw_data_len = tcp_sock.recv(4)
        data_len = struct.unpack('>I', raw_data_len)[0]

        data = b''

        while len(data) < data_len:
            packet = tcp_sock.recv(data_len - len(data))
            data += packet

        data = data.decode('ascii')
        print(data)
