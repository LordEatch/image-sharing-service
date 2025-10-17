from socket import socket, AF_INET, SOCK_STREAM
from ..utilities import socket_utilities

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 65531


def run_client() -> None:
    my_socket = open_client_socket(SERVER_HOST, SERVER_PORT)
    with my_socket:
        payload = input("Enter message > ")
        socket_utilities.send_payload(my_socket, payload)

def open_client_socket(host: str, port: int) -> socket:
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((host, port))
    return client_socket