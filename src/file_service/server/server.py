from socket import socket, AF_INET, SOCK_STREAM
from typing import Any
from ..socket_utils import socket_utils

HOST = "127.0.0.1"
PORT = 65531


def run_server() -> None:
    with open_listening_socket(HOST, PORT) as listening_socket:
        handle_clients(listening_socket)

def open_listening_socket(host: str, port: int) -> socket:
    listening_socket = socket(AF_INET, SOCK_STREAM)
    listening_socket.bind((host, port))
    listening_socket.listen()
    print(f"Server listening on {host}:{port}.")
    return listening_socket

def handle_clients(listening_socket: socket) -> None:
    """
    Take an open listening socket as a parameter. Loop over each client connection and handle them.
    """
    # WARNING Will this break if 2 clients connect at the same time?
    while True:
        try:
            client_socket, client_address = listening_socket.accept()
            handle_client(client_socket, client_address)
        except ConnectionError:
            print("Connection closed.")

def handle_client(client_socket: socket, client_address: tuple[str, int]) -> None:
    """
    Take an open client socket as a parameter. Loop over each message and handle them.
    """
    print(f"{client_address} has connected.")
    with client_socket:
        # Cycle over each message until the client disconnects.
        while True:
            try:
                handle_message(client_socket)
            except ConnectionError:
                print(f"{client_address} has disconnected.")
                break

def handle_message(client_socket: socket) -> Any:
    """
    Take an open client socket as a parameter. Receive the socket's next message in full.
    """
    incoming_payload = socket_utils.receive_payload(client_socket)
    print(f"Received: {incoming_payload}")
    return incoming_payload


if __name__ == "__main__":
    run_server()
