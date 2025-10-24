from socket import socket
from typing import Any

from file_service.utilities import storage, message as message_utilities
from file_service.protocol import message as message_protocol
from file_service.protocol.message import (
    COMMAND_KEY,
    FILENAME_KEY,
    FILE_DATA_KEY,
    PUT_VAL,
    GET_VAL,
    LIST_VAL,
    OK_VAL,
    ERROR_VAL,
    CommandError,
)
from file_service.utilities.debug import print_debug, print_error, print_command_report


def handle_request(sock: socket) -> None:
    """Handle a single client request and perform the corresponding action."""
    request = message_utilities.receive_message(sock)
    command = request[COMMAND_KEY]
    print_debug(f"Received a request with command: {command}.")

    if command == PUT_VAL:
        handle_put_request(sock, request)
    elif command == GET_VAL:
        handle_get_request(sock, request)
    elif command == LIST_VAL:
        handle_list_request(sock, request)
    else:
        raise CommandError(f"Unknown command received from client: {command}.")


def handle_put_request(sock: socket, request: dict[str, Any]) -> None:
    """Handle a PUT request from the client."""
    filename, file_data = request[FILENAME_KEY], request[FILE_DATA_KEY]
    try:
        storage.save_local_file(filename, file_data)
    except (ValueError, FileExistsError) as e:
        error_messages = {
            ValueError: f"Cannot save '{filename}' on the server because it is empty",
            FileExistsError: f"Cannot save '{filename}' on the server since it already exists",
        }
        error_message = error_messages[type(e)]
        print_error(error_message)
        print_command_report(sock, PUT_VAL, False, filename, error_message)
        _send_error_response(sock, request, error_message)
        return

    print_command_report(sock, PUT_VAL, True, filename)
    _send_ok_response(sock, request)


def handle_get_request(sock: socket, request: dict[str, Any]) -> None:
    """Handle a GET request from the client."""
    filename = request[FILENAME_KEY]
    try:
        file_data = storage.get_local_file(filename)
    except FileNotFoundError:
        error_message = f"Cannot find '{filename}' on the server"
        print_error(error_message)
        print_command_report(sock, GET_VAL, False, filename, error_message)
        _send_error_response(sock, request, error_message)
        return

    print_command_report(sock, GET_VAL, True, filename)
    _send_ok_response(sock, request, file_data=file_data)


def handle_list_request(sock: socket, request: dict[str, Any]) -> None:
    """Handle a LIST request from the client."""
    filenames = storage.get_local_list()

    if not filenames:
        error_message = "There are no local files or directories stored on the server"
        print_command_report(sock, LIST_VAL, False, error_message=error_message)
        _send_error_response(sock, request, error_message)

    print_command_report(sock, LIST_VAL, True)
    _send_ok_response(sock, request, details="\n".join(filenames))



def _send_ok_response(
    sock: socket,
    request: dict[str, Any],
    details: str | None = None,
    file_data: bytes | None = None,
) -> None:
    """Send a success response to the client."""
    _send_response(sock, request, OK_VAL, details, file_data)


def _send_error_response(sock: socket, request: dict[str, Any], error_message: str) -> None:
    """Send an error response to the client."""
    _send_response(sock, request, ERROR_VAL, error_message)


def _send_response(
    sock: socket,
    request: dict[str, Any],
    status: str,
    details: str | None = None,
    file_data: bytes | None = None,
) -> None:
    """Send a response message to the client."""
    payload = message_protocol.construct_payload(
        request[COMMAND_KEY],
        status,
        details,
        request[FILENAME_KEY],
        file_data,
    )
    message_utilities.send_message(sock, payload)
