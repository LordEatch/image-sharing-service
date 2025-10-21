from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from typing import Any
from ..utilities import socket_utilities

HOST = "localhost"


def run_server(port: int) -> None:
    """
    Start the server and handle incoming client connections.
    """
    with open_listening_socket(HOST, port) as listening_socket:
        handle_clients(listening_socket)


def open_listening_socket(host: str, port: int) -> socket:
    """
    Open and configure a TCP listening socket for the server.
    """
    listening_socket = socket(AF_INET, SOCK_STREAM)

    # Set SO_REUSEADDR to allow immediate reuse of the address/port. This prevents "Address already in use" errors when
    # the socket is in the TIME_WAIT state from a previous connection (even if the port is no longer actively used).
    listening_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    listening_socket.bind((host, port))
    listening_socket.listen()

    print(f"Server listening on {host}:{port}.")
    return listening_socket


def handle_clients(listening_socket: socket) -> None:
    """
    Continuously accept and handle incoming client connections.
    """
    # WARNING:
    # This may block if multiple clients attempt to connect simultaneously.

    while True:
        try:
            client_socket, client_address = listening_socket.accept()
            handle_client(client_socket, client_address)
        except ConnectionError:
            print("Connection closed.")


def handle_client(client_socket: socket, client_address: tuple[str, int]) -> None:
    """
    Handle communication with a single connected client.
    """
    print(f"{client_address} has connected.")
    with client_socket:
        # Process each message until the client disconnects.
        while True:
            try:
                handle_message(client_socket)
            except ConnectionError:
                print(f"{client_address} has disconnected.")
                break


def handle_message(client_socket: socket) -> Any:
    """
    Receive and process the next message from the client socket.
    """
    incoming_payload = socket_utilities.receive_payload(client_socket)
    print(f"Received: {incoming_payload}")
    return incoming_payload
