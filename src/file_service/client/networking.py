from socket import socket, AF_INET, SOCK_STREAM

from file_service.client import client_io, commands


def run_client(server_host: str, server_port: int) -> None:
    """Start the client and handle a single command."""
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((server_host, server_port))
    with sock:
        command = client_io.get_command()
        commands.handle_command(
            sock,
            command,
            client_io.get_file_str,  # Pass the function itself.
        )
