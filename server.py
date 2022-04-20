import socket
import subprocess
import os
from logging import Logger as logg
from encrypt import decryptAES # Local

PORT, USER_NUM = 4243, 1
HOST = 'localhost'

ec = subprocess.run(['python', '.\key_gen.py'])

if not ec.returncode:
    logg.info(f'.\key_gen.py create key pair at {os.getcwd}')
    
else:
    logg.warning(f'.\key_gen.py CANNO RUN at {os.getcwd}')
    
sock = socket.socket() # Create socket

sock.bind(('', PORT))
sock.listen(USER_NUM) # Set connection listener limit
conn, addr = sock.accept()
PRK_NAME = 'prk.key'

while True:
    
    data = conn.recv(4096)# Partition data-block    
    data = decryptAES(data, PRK_NAME)
    
    if data:
        conn.send(b'OK 200')
    
    else:
        conn.send(b'BAD 404')
        logg.warning(f'.\server.py get "BAD 404" code at {os.getcwd}')
    
    print(f"RCV: {data}") # Terminal OUT
    
    if data == "\DONE":
        logg.warning(f'.\server.py stop work at {os.getcwd}')
        break
    
conn.close()