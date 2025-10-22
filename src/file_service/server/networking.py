from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from . import request_handling

_HOST = "localhost"


def run_server(port: int) -> None:
    """Start the server and handle incoming client connections."""
    listening_socket = socket(AF_INET, SOCK_STREAM)

    # Set SO_REUSEADDR to allow immediate reuse of the address/port. This prevents "Address already in use" errors
    # when the socket is in the TIME_WAIT state from a previous connection (even if the port is no longer actively
    # used).
    listening_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    listening_socket.bind((_HOST, port))
    listening_socket.listen()

    print(f"Server listening on {_HOST}:{port}...")

    with listening_socket:
        handle_clients(listening_socket)


def handle_clients(listening_socket: socket) -> None:
    """Continuously accept and handle incoming client connections 1 at a time."""
    while True:
        try:
            client_socket, client_address = listening_socket.accept()
            handle_client(client_socket, client_address)
        except KeyboardInterrupt:
            print("Server shutting down...")
            break


def handle_client(client_socket: socket, client_address: tuple[str, int]) -> None:
    """Continuously receive and handle incoming messages from a client socket until it disconnects."""
    print(f"{client_address} has connected.")
    with client_socket:
        # Process each message until the client disconnects.
        while True:
            try:
                request_handling.handle_request(client_socket)
            except ConnectionError:
                print(f"{client_address} has disconnected.")
                break