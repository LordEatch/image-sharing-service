from socket import socket
from typing import Callable, Any
import os

from ..utilities.message_protocol import (
    PUT_VAL, GET_VAL, LIST_VAL, REQUEST_VAL, STATUS_KEY,
    COMMAND_KEY, OK_VAL
)
from ..utilities.debug import print_debug
from ..utilities import storage, socket_utilities


def handle_command(sock: socket, command: str, get_file_str_fn: Callable[[], str]) -> None:
    """Dispatch a client command to the appropriate handler."""
    handlers = {
        PUT_VAL: handle_put_command,
        GET_VAL: handle_get_command,
        # LIST_VAL: handle_list_command
    }
    handler = handlers[command]
    handler(sock, get_file_str_fn)


def handle_put_command(sock: socket, get_file_str_fn: Callable[[], str]) -> None:
    """Send a PUT request to upload a file to the server."""
    filepath = get_file_str_fn()
    filename = os.path.basename(filepath)
    file_data = storage.get_file_binary(filepath)

    print_debug(f"Sending {PUT_VAL} request for '{filename}'...")
    socket_utilities.send_message(sock, PUT_VAL, REQUEST_VAL, filename, file_data)
    print_debug(f"{PUT_VAL} request for '{filename}' sent successfully.")

    # response = _receive_response(sock, PUT_VAL)
    # debug_print(f"Server response: {response}")


def handle_get_command(sock: socket, get_file_str_fn: Callable[[], str]) -> None:
    """Send a GET request to download a file from the server."""
    filename = get_file_str_fn()

    print_debug(f"Sending {GET_VAL} request for '{filename}'...")
    socket_utilities.send_message(sock, GET_VAL, REQUEST_VAL, filename)
    print_debug(f"{GET_VAL} request for '{filename}' sent successfully.")

    # response = _receive_response(sock, GET_VAL)
    # debug_print(f"Server response: {response}")


def _receive_response(sock: socket, expected_command: str) -> dict[str, Any]:
    """Receive and validate a server response."""
    response = socket_utilities.receive_message(sock)
    _validate_response(response, expected_command)
    return response


def _validate_response(response: dict[str, Any], expected_command: str) -> None:
    """Ensure the server response matches the expected command and has an OK status."""
    response_command = response.get(COMMAND_KEY)
    response_status = response.get(STATUS_KEY)

    if response_command != expected_command or response_status != OK_VAL:
        raise ConnectionError(f"{expected_command} failed. Response status: {response_status}.")

    print_debug(f"{expected_command} completed successfully. Response status: {response_status}.")
