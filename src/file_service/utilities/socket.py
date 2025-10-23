from socket import socket

from file_service.utilities.debug import print_debug, print_error


def send_data(sock: socket, data: bytes) -> None:
    """Send all bytes of data through a socket."""
    print_debug(
        "Sending data to socket..."
        f"\n\tSize: {len(data)} bytes."
        f"\n\tSocket: {sock}."
    )

    try:
        sock.sendall(data)  # Send all the data to the socket.
    except ConnectionError:
        print_error("Connection closed before all data was sent.")
        return

    print_debug("Payload sent.")


def receive_data(sock: socket, max_byte_count: int) -> bytes:
    """Receive a fixed number of bytes from a socket."""
    # socket.recv() may return fewer bytes than requested due to network latency.
    print_debug(
        f"Receiving {max_byte_count} bytes from the socket..."
        f"\n\tSocket: {sock}."
    )

    data = b""
    # Continue until all expected bytes are received.
    while len(data) < max_byte_count:
        leftover_bytes = max_byte_count - len(data)

        print_debug(
            "Calling recv()..."
            f"\n\tLeftover bytes: {leftover_bytes}"
        )

        packet = sock.recv(leftover_bytes)
        if not packet:
            print_debug("The next packet is empty, indicating the connection closed.")
            raise ConnectionError("Connection closed.")

        data += packet

    print_debug("Received all bytes from the socket.")
    return data
