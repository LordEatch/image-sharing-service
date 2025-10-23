from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

from file_service.server import requests
from file_service.utilities.debug import print_error

_HOST = "0.0.0.0"


def run_server(port: int) -> None:
    """Start the server and handle incoming client connections."""
    listening_socket = socket(AF_INET, SOCK_STREAM)

    # Allow immediate reuse of the address and port to prevent
    # "Address already in use" errors when restarting the server.
    listening_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    try:
        _validate_port(port)
    except (ValueError, OSError) as e:
        error_messages = {
            ValueError: str(e),
            OSError: f"Port {port} is already in use or unavailable."
        }
        error_message = error_messages[type(e)]
        print_error(error_message)
        return

    listening_socket.bind((_HOST, port))
    listening_socket.listen()
    print(f"Server up and running on {_HOST}:{port}...")

    with listening_socket:
        handle_clients(listening_socket)


def handle_clients(listening_socket: socket) -> None:
    """Accept and handle client connections one at a time."""
    while True:
        client_socket, client_address = listening_socket.accept()
        handle_client(client_socket, client_address)


def handle_client(client_socket: socket, client_address: tuple[str, int]) -> None:
    """Handle messages from a connected client until disconnection."""
    print(f"{client_address} has connected.")
    with client_socket:
        while True:
            try:
                requests.handle_request(client_socket)
            except ConnectionError:
                print(f"{client_address} has disconnected.")
                break


def _validate_port(port: int) -> None:
    """Validate that a port is within range and available."""
    _MIN_PORT = 1
    _MAX_PORT = 65535

    if not _MIN_PORT <= port <= _MAX_PORT:
        raise ValueError(f"Port must be between {_MIN_PORT} and {_MAX_PORT}.")

    # Raises OSError if the port is already in use or unavailable.
    with socket(AF_INET, SOCK_STREAM) as test_socket:
        test_socket.bind((_HOST, port))
