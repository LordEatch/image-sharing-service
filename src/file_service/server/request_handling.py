from socket import socket
from typing import Any

from ..utilities import socket_utilities, storage
from ..utilities.debug import print_debug, print_error
from ..utilities.message_protocol import (
    COMMAND_KEY, STATUS_KEY, FILENAME_KEY, FILE_DATA_KEY,
    PUT_VAL, GET_VAL, LIST_VAL, REQUEST_VAL, OK_VAL, ERROR_VAL
)


def handle_request(sock: socket) -> None:
    """Handle a client request and perform the requested action."""
    request = socket_utilities.receive_message(sock)
    command = request.get(COMMAND_KEY, "Unrecognised command")
    print_debug(f"Received a request with command: {command}")
    print_error(f"test")

    if command == PUT_VAL:
        # handle_put_request(sock, request)
        pass
    elif command == GET_VAL:
        # handle_get_request(sock, request)
        pass
    elif command == LIST_VAL:
        # handle_list_request(sock)
        pass
    else:
        print_error(f"Unknown command received: {command}")
        socket_utilities.send_message(sock, command, ERROR_VAL, "Unknown command")