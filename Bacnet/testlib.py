import json
import socket
import requests


def read_json_file(filename: str):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


def write_json_file(filename: str, data: dict):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def is_connected(url):
    try:
        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Set a timeout for connection attempts
        client_socket.settimeout(10)

        # Connect to the server
        client_socket.connect((socket.gethostname(), 8888))

        # Send data to the server
        message = "Hello, Server!"
        client_socket.send(message.encode())

        # Receive and print the server's response
        response = client_socket.recv(1024)
        print(f"Server response: {response.decode()}")
    except socket.timeout:
        print("Connection timed out.")
    except Exception as e:
        print(f"Error in client: {str(e)}")
    finally:
        # Close the client socket
        client_socket.close()
        
def is_connectedold3(url, port=0):
    try:
        _sock = socket.create_connection((url, port), 2)
        if _sock is not None:
            print('Connection Active.')
            _sock.close()
        return True
    #except OSError:
    #    print('OSError: Connection cannot be established')
    except Exception as e:
     print("Connection Error: " + str(e))
    return False

def is_connected4(url, port=0):
    try:
        _sock = socket.create_connection((url, port), timeout=5)
        if _sock is not None:
            print('Connection Active.')
            _sock.close()
        return True
    except socket.timeout:
        print('Connection Timeout: Unable to establish a connection within the specified time.')
    except ConnectionRefusedError:
        print('Connection Refused: The server actively rejected the connection request.')
    except Exception as e:
        print(f"Connection Error: {str(e)}")
    return False


def is_connectedold(url):
    try:
        addr_info = socket.getaddrinfo(url, None)
        print(f"Address: %s" % addr_info)
        for addr in addr_info:
            _sock = socket.create_connection(addr[4], 2)
            if _sock is not None:
                print('Connection Active.')
                _sock.close()
                return True
    except OSError:
        print('OSError: Connection cannot be established')
    except Exception as e:
        print(e)
    return False

def post_api(_url: str, payload: dict):
    try:
        res = requests.post(_url, payload)
    except Exception as e:
        print(e)
        return
    else:
        print(res.json())
    return res
