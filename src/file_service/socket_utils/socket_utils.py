from socket import socket
from typing import Any
from . import message_protocol

DEBUG = False


def send_payload(my_socket: socket, payload: Any) -> None:
    """
    Send a python object framed in a message defined by the protocol to a socket.
    """
    message_binary = message_protocol.frame_message(payload)
    my_socket.sendall(message_binary)

def receive_payload(my_socket: socket) -> Any:
    """
    Receive an ENTIRE python object framed in a message defined by the protocol from a socket.
    """
    def receive_all_binary_from_my_socket(max_number_of_bytes: int) -> bytes:
        return receive_all_binary(my_socket, max_number_of_bytes)

    # NOTE
    # A function that receives all binary from a SPECIFIC socket is passed to message_protocol.unframe_message() because the message protocol needs to choose how much binary to receive from the socket.
    # If the socket were passed to the message protocol then the message protocol would have to know about the socket (bad encapsulation).
    # If the message protocol logic were defined here then it would not belong.

    return message_protocol.unframe_message(receive_all_binary_from_my_socket)


def receive_all_binary(my_socket: socket, max_number_of_bytes: int) -> bytes:
    """
    Receive max_number_of_bytes bytes from a socket. Raise an exception if the connection is closed.
    """
    # NOTE
    # This is necessary because recv() may only receive a few bytes because of network latency.
    # So we repeat recv() until we have received n bytes.
    data = b""
    # Repeat until we have received n bytes.
    while len(data) < max_number_of_bytes:
        leftover_bytes = max_number_of_bytes - len(data)
        if DEBUG:
            print(f"DEBUG: Calling recv() from within receive_all_binary() to get {max_number_of_bytes} bytes from the the socket {my_socket}.")
        packet = my_socket.recv(leftover_bytes)
        if not packet:
            if DEBUG:
                print("DEBUG: The next packet is empty so the connection closed.")
            raise ConnectionError("Connection closed.")
        data += packet
    return data