import os
from socket import socket
from typing import Callable, Any

from file_service.utilities import storage, message as message_utilities
from file_service.protocol import message as message_protocol
from file_service.protocol.message import (
    PUT_VAL,
    GET_VAL,
    LIST_VAL,
    FILE_DATA_KEY,
    STATUS_KEY,
    ERROR_VAL,
    DETAILS_KEY,
)
from file_service.utilities.debug import print_debug, print_error, print_command_report


def handle_command(sock: socket, command: str, get_file_str_fn: Callable[[], str]) -> None:
    """Dispatch a client command to the appropriate handler."""
    print_debug(f"Received the command: {command}.")

    def equals_ignore_case(a: str, b: str) -> bool:
        return a.casefold() == b.casefold()

    if equals_ignore_case(command, PUT_VAL):
        handle_put_command(sock, get_file_str_fn)
    elif equals_ignore_case(command, GET_VAL):
        handle_get_command(sock, get_file_str_fn)
    elif equals_ignore_case(command, LIST_VAL):
        handle_list_command(sock)
    else:
        print_error(f"Unknown command received: {command}.")


def handle_put_command(sock: socket, get_file_str_fn: Callable[[], str]) -> None:
    """Upload a file to the server."""
    filepath = get_file_str_fn()
    filename = os.path.basename(filepath)

    try:
        file_data = storage.get_image(filepath)
    except (ValueError, FileNotFoundError) as e:
        error_messages = {
            ValueError: str(e),
            FileNotFoundError: f"Cannot save '{filename}' on the server since it already exists",
        }
        error_message = error_messages[type(e)]
        print_error(error_message)
        print_command_report(sock, PUT_VAL, False, filename, error_message)
        return

    print_debug(f"Sending {PUT_VAL} request for '{filename}'...")
    response = _send_request(sock, command=PUT_VAL, filename=filename, file_data=file_data)
    print_debug(f"{PUT_VAL} request for '{filename}' sent successfully.")

    success = response[STATUS_KEY] != ERROR_VAL
    print_command_report(sock, PUT_VAL, success, filename, response.get(DETAILS_KEY))


def handle_get_command(sock: socket, get_file_str_fn: Callable[[], str]) -> None:
    """Download a file from the server."""
    filename = get_file_str_fn()

    print_debug(f"Sending {GET_VAL} request for '{filename}'...")
    response = _send_request(sock, command=GET_VAL, filename=filename)
    print_debug(f"{GET_VAL} request for '{filename}' sent successfully.")

    if response[STATUS_KEY] == ERROR_VAL:
        print_command_report(sock, GET_VAL, False, filename, response[DETAILS_KEY])
        return

    try:
        storage.save_local_file(filename, response[FILE_DATA_KEY])
    except FileExistsError:
        msg = f"Cannot download '{filename}' because it already exists on the client."
        print_error(msg)
        print_command_report(sock, GET_VAL, False, filename, msg)
        return

    print_command_report(sock, GET_VAL, True, filename)


def handle_list_command(sock: socket) -> None:
    """
    Get a list of all files and directories stored on the server.
    Print them 1 line at a time.
    Print an error message if no files are stored.
    """
    response = _send_request(sock, command=LIST_VAL)

    if response[STATUS_KEY] == ERROR_VAL:
        print_command_report(sock, GET_VAL, False, error_message=response[DETAILS_KEY])
        return

    filenames = response[DETAILS_KEY]

    print("Files or directories on the server:")
    print(filenames)  # The filenames are send by the server as a single string with line breaks between files.

    print_command_report(sock, LIST_VAL, True)


def _send_request(sock: socket, **kwargs) -> dict[str, Any]:  # type: ignore
    """Send a request to the server and return its response."""
    payload = message_protocol.construct_payload(**kwargs)
    message_utilities.send_message(sock, payload)
    return message_utilities.receive_message(sock)
