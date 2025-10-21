from socket import socket
from typing import Any
from . import message_protocol

DEBUG = False


def send_payload(my_socket: socket, payload: Any) -> None:
    """
    Send a Python object framed in a message defined by the protocol to a socket.
    """
    # Convert the payload into a framed binary message.
    message_binary = message_protocol.frame_message(payload)

    # Send the entire binary message over the socket.
    my_socket.sendall(message_binary)


def receive_payload(my_socket: socket) -> Any:
    """
    Receive an entire Python object framed in a message defined by the protocol from a socket.
    """
    def receive_all_binary_from_my_socket(max_number_of_bytes: int) -> bytes:
        return receive_all_binary(my_socket, max_number_of_bytes)

    # NOTE:
    # A function that receives all binary from a specific socket is passed to message_protocol.unframe_message(). This
    # allows the message protocol to control how much binary to read without needing direct access to the socket. This
    # preserves proper encapsulation and keeps protocol logic separate from socket handling.

    return message_protocol.unframe_message(receive_all_binary_from_my_socket)


def receive_all_binary(my_socket: socket, max_number_of_bytes: int) -> bytes:
    """
    Receive the specified number of bytes from a socket.
    Raise an exception if the connection is closed before all bytes are received.
    """
    # NOTE:
    # This function is necessary because socket.recv() may return fewer bytes than requested due to network latency.

    data = b""

    # Repeat until the full number of bytes is received.
    while len(data) < max_number_of_bytes:
        leftover_bytes = max_number_of_bytes - len(data)
        if DEBUG:
            print(f"DEBUG: Calling recv() to get {max_number_of_bytes} bytes from socket {my_socket}.")
        packet = my_socket.recv(leftover_bytes)
        if not packet:
            if DEBUG:
                print("DEBUG: The next packet is empty, indicating the connection closed.")
            raise ConnectionError("Connection closed.")
        data += packet

    return data
