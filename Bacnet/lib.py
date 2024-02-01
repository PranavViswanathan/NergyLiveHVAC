import json
import socket
import requests


def is_valid_url(url):
    try:
        response = requests.head(url)
        print(f"Connection from dahboard with response {response} has been established.")
        return response.status_code < 400
    except requests.ConnectionError:
        return False

def read_json_files(filename: str):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data
def read_json_file(filename: str):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found - {filename}")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in file - {filename}")
    except Exception as e:
        print(f"Error: {e}")


def write_json_file(filename: str, data: dict):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)


def is_connectedold(url, port=''):
    try:
        _sock = socket.create_connection((url, port), 2)
        if _sock is not None:
            print('Connection Active.')
            _sock.close()
        return True
    except OSError:
        print('OSError: Connection cannot be established')
    except Exception as e:
        print(e)
    return False


def is_connected(url):

    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = 0
        print(f"{url}")
        url = "https://dashboard.nergylive.com"
        server_socket.bind((url, port))
        assigned_port = server_socket.getsockname()[1]
        print(f"Server listening on {url}:{assigned_port}")
        server_socket.listen(5)
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        message = "Hello, client! Thanks for connecting."
        client_socket.send(message.encode())

        if client_socket is not None:
            print('Connection active')
            client_socket.close()
            server_socket.close()
        return True
        #_sock = socket.create_connection((url, 0 ), 2)
        #if _sock is not None:
        #    print('Connection Active.')
        #    _sock.close()
        #return True
    #except OSError:
    #    print('OSError: Connection cannot be established')
    #except Exception as e:
    except socket.error as e:
        print(f" socket error : {e}")
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
