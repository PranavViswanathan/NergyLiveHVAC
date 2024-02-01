import json
import socket
import requests

HOSTNAME = 'dashboard.nergylive.com'
host = f'https://{HOSTNAME}/Api/add_data'
port = '443'
try:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host,port))
    server_socket.listen(5)
    print(f"server listens to address {host}:{port}")
    client_socket, addr  = server_socket.accept()
    print(f"socket listens to address: {addr}")
    if client_socket is not None:
        print('Connection Active.')
        _sock.close()
except OSError:
    print('OSError: Connection cannot be established')
except Exception as e:
    print(e)
