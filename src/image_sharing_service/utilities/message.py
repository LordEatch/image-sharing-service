from socket import socket
from typing import Any

from file_service.protocol import socket as socket_protocol
from file_service.utilities import socket as socket_utilities


def send_message(sock: socket, payload: dict[str, Any]) -> None:
    """Send a framed message through a socket."""
    message = socket_protocol.frame_message(payload)
    socket_utilities.send_data(sock, message)


def receive_message(sock: socket) -> dict[str, Any]:
    """Receive and unframe a message from a socket."""
    def receive_data_from_sock(byte_count: int) -> bytes:
        return socket_utilities.receive_data(sock, byte_count)

    payload: dict[str, Any] = socket_protocol.unframe_message(receive_data_from_sock)
    return payload
