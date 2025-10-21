from socket import socket, AF_INET, SOCK_STREAM
from ..utilities import socket_utilities


def run_client(server_host: str, server_port: int) -> None:
    """
    Run the client program.
    """
    my_socket = open_client_socket(server_host, server_port)
    with my_socket:
        payload = input("Enter message > ")
        socket_utilities.send_payload(my_socket, payload)


def open_client_socket(host: str, port: int) -> socket:
    """
    Open a TCP client socket and connect it to the specified server.
    """
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((host, port))
    return client_socket
