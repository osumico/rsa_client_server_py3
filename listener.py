import socket
from encrypt import encryptAES # Local

sock = socket.socket()
PORT = 4243
HOST = 'localhost'
sock.connect((HOST, PORT))

PBK_NAME = 'pbk.key'

while True:
    
    data_in = input("PTXT_IN: ") # Terminal IN
    data_in = encryptAES(data_in, PBK_NAME)   
    sock.send(data_in)
    
    resp = sock.recv(4096)
    print(f'RSP: {resp.decode()}')