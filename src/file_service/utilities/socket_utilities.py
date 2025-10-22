from socket import socket
from typing import Any
from . import message_protocol
from .debug import print_debug


def send_message(
        sock: socket,
        command: str,
        status: str,
        filename: str | None = None,
        file_data: bytes | None = None
) -> None:
    payload = {
        message_protocol.COMMAND_KEY: command,
        message_protocol.FILENAME_KEY: filename,
        message_protocol.STATUS_KEY: status,
        message_protocol.FILE_DATA_KEY: file_data
    }
    _send_payload(sock, payload)


def receive_message(sock: socket) -> dict[str, Any]:
    return _receive_payload(sock)


def _send_payload(sock: socket, payload: dict[str, Any]) -> None:
    """Send a Python object framed in a message defined by the protocol to a socket."""
    print_debug(f"Sending payload to socket...\n\tpayload: {payload}\n\tsocket: {sock}")
    message_binary = message_protocol.frame_message(payload)  # Frame the payload with the message protocol into binary.
    sock.sendall(message_binary)  # Send ALL of message_binary to the socket.
    print_debug(f"Payload sent.")


def _receive_payload(sock: socket) -> dict[str, Any]:
    """Receive an entire Python object framed in a message defined by the protocol from a socket."""
    # A function that receives all binary from a specific socket is passed to message_protocol.unframe_message(). This
    # allows the message protocol to control how much binary to read without needing direct access to the socket. This
    # preserves proper encapsulation and keeps protocol logic separate from socket handling.

    def receive_all_binary_from_sock(max_number_of_bytes: int) -> bytes:
        return _receive_all_binary(sock, max_number_of_bytes)

    return message_protocol.unframe_message(receive_all_binary_from_sock)


def _receive_all_binary(my_socket: socket, max_number_of_bytes: int) -> bytes:
    """
    Receive the specified number of bytes from a socket.
    Raise an exception if the connection is closed before all bytes are received.
    """
    # This function is necessary because socket.recv() may return fewer bytes than requested due to network latency.

    data = b""
    # Repeat until the full number of bytes is received.
    while len(data) < max_number_of_bytes:
        leftover_bytes = max_number_of_bytes - len(data)
        print_debug(f"Calling recv() to get {max_number_of_bytes} bytes from socket...\n\tsocket: {my_socket}\n\tleftover_bytes: {leftover_bytes}")
        packet = my_socket.recv(leftover_bytes)
        if not packet:
            print_debug("The next packet is empty, indicating the connection closed.")
            raise ConnectionError("Connection closed.")
        data += packet
    return data
