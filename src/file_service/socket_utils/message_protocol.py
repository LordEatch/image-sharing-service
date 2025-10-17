from typing import Literal, Any, Callable
import pickle  # pickle is used to (de)serialise python objects for binary transmission.

NUMBER_OF_PAYLOAD_LENGTH_BYTES = 2
ENDIANNESS: Literal["big", "little"] = "big"


# WARNING
# Break some of these functions down into smaller functions.

def get_max_number_of_payload_bytes() -> int:
    """
    Return the max number of payload bytes that can be sent given NUMBER_OF_PAYLOAD_LENGTH_BYTES.
    """
    number_of_payload_length_bits = 8 * NUMBER_OF_PAYLOAD_LENGTH_BYTES
    max_number_of_payload_bytes: int = 2 ** number_of_payload_length_bits - 1
    return max_number_of_payload_bytes

def frame_message(payload: Any) -> bytes:
    """
    Return a binary message containing a payload ready for transmission. If the payload is too large then raise an exception.
    """
    payload_binary = pickle.dumps(payload)
    number_of_payload_bytes = len(payload_binary)

    # Check if the payload is too large to send given the number of prefix bytes.
    max_number_of_payload_bytes = get_max_number_of_payload_bytes()
    if number_of_payload_bytes > max_number_of_payload_bytes:
        raise ValueError(f"Payload too large. Max size is {max_number_of_payload_bytes} bytes.")

    payload_length_binary = number_of_payload_bytes.to_bytes(NUMBER_OF_PAYLOAD_LENGTH_BYTES, ENDIANNESS)
    message_binary = payload_length_binary + payload_binary
    return message_binary

def unframe_message(receive_all_binary_from_socket_fn: Callable[[int], bytes]) -> Any:
    """
    Return a python object from a framed message defined by the protocol from a socket.
    """
    # Read the payload length prefix.
    payload_length_binary = receive_all_binary_from_socket_fn(NUMBER_OF_PAYLOAD_LENGTH_BYTES)
    number_of_payload_bytes = int.from_bytes(payload_length_binary, ENDIANNESS)

    # Read the payload itself.
    payload_binary = receive_all_binary_from_socket_fn(number_of_payload_bytes)
    # Deserialise.
    payload = pickle.loads(payload_binary)
    return payload