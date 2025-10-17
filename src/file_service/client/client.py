from socket import socket, AF_INET, SOCK_STREAM
from ..socket_utils import socket_utils

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 65531


def main() -> None:
    my_socket = open_client_socket(SERVER_HOST, SERVER_PORT)
    with my_socket:
        payload = input("Enter message > ")
        socket_utils.send_payload(my_socket, payload)

def open_client_socket(host: str, port: int) -> socket:
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((host, port))
    return client_socket


if __name__ == "__main__":
    main()