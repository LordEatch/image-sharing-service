from socket import socket
import sys

from file_service.utilities.debug import print_debug


def print_response_report(
    sock: socket,
    command: str,
    success: bool,
    filename: str | None = None,
    error_message: str | None = None,
) -> None:
    """Print a formatted response report from the server."""
    _SUCCESS_VAL = "SUCCESS"
    _FAILURE_VAL = "FAILURE"

    status = _SUCCESS_VAL if success else _FAILURE_VAL
    host = sock.getpeername()
    parts = [str(host), command]
    if filename:
        parts.append(filename)
    parts.append(status)

    report = "\t".join(parts)
    if not success and error_message:
        report += f": {error_message}."
    print(report)


# Erroneous user inputs are not caught because the brief did not specify that such validation was required.

def get_server_host() -> str:
    """Retrieve the server host from command-line arguments."""
    host = sys.argv[1]
    print_debug(f"User inputted server host: {host}.")
    return host


def get_server_port() -> int:
    """Retrieve the server port from command-line arguments."""
    port = int(sys.argv[2])
    print_debug(f"User inputted server port: {port}.")
    return port


def get_command() -> str:
    """Retrieve the command from command-line arguments."""
    command = sys.argv[3]
    print_debug(f"User inputted command: {command}.")
    return command


def get_file_str() -> str:
    """Retrieve the filename or filepath from command-line arguments."""
    file_string = sys.argv[4]
    print_debug(f"User inputted file string: {file_string}.")
    return file_string
