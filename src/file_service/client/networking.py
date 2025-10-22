from socket import socket, AF_INET, SOCK_STREAM
from . import client_io, command_handling


def run_client(server_host: str, server_port: int) -> None:
    """Run the client program."""
    sock = open_client_socket(server_host, server_port)
    with sock:
        command = client_io.get_command()
        command_handling.handle_command(
            sock,
            command,
            client_io.get_file_str,  # Pass the function itself.
        )


def open_client_socket(host: str, port: int) -> socket:
    """Open a TCP client socket and connect it to the specified server."""
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((host, port))
    return sock