from typing import Literal, Any, Callable
import pickle  # pickle is used to (de)serialise Python objects for binary transmission.

_NUMBER_OF_PAYLOAD_LENGTH_BYTES = 2
_ENDIANNESS: Literal["big", "little"] = "big"


def unframe_message(receive_all_binary_from_socket_fn: Callable[[int], bytes]) -> Any:
    """
    Return a Python object from a framed message defined by the protocol from a socket.
    """
    # Receive the payload length in binary form.
    payload_length_binary = receive_all_binary_from_socket_fn(_NUMBER_OF_PAYLOAD_LENGTH_BYTES)

    # Convert the payload length from binary to an integer.
    number_of_payload_bytes = int.from_bytes(payload_length_binary, _ENDIANNESS)

    # Receive the payload itself.
    payload_binary = receive_all_binary_from_socket_fn(number_of_payload_bytes)

    # Deserialise the payload back into a Python object.
    payload = pickle.loads(payload_binary)
    return payload


def frame_message(payload: Any) -> bytes:
    """
    Return a binary message containing a payload ready for transmission.
    Raise an exception if the payload is too large.
    """
    # Serialise the payload into binary form.
    payload_binary = pickle.dumps(payload)
    number_of_payload_bytes = len(payload_binary)

    # Check if the payload exceeds the maximum allowed size.
    max_number_of_payload_bytes = get_max_number_of_payload_bytes(_NUMBER_OF_PAYLOAD_LENGTH_BYTES)
    if number_of_payload_bytes > max_number_of_payload_bytes:
        raise ValueError(f"Payload too large. Max size is {max_number_of_payload_bytes} bytes.")

    # Convert the payload length to binary and prepend it to the payload.
    payload_length_binary = number_of_payload_bytes.to_bytes(_NUMBER_OF_PAYLOAD_LENGTH_BYTES, _ENDIANNESS)
    message_binary = payload_length_binary + payload_binary
    return message_binary


def get_max_number_of_payload_bytes(number_of_payload_length_bytes: int) -> int:
    """
    Return the maximum number of payload bytes that can be sent given the number of payload length bytes.
    """
    def check_number_of_payload_length_bytes() -> None:
        """
        Check that number_of_payload_length_bytes is within the valid range.
        Raise an exception if it is not.
        """
        _MIN_NUMBER_OF_PAYLOAD_LENGTH_BYTES = 1
        _MAX_NUMBER_OF_PAYLOAD_LENGTH_BYTES = 8

        is_valid = _MIN_NUMBER_OF_PAYLOAD_LENGTH_BYTES <= number_of_payload_length_bytes <= _MAX_NUMBER_OF_PAYLOAD_LENGTH_BYTES
        if not is_valid:
            raise ValueError("number_of_payload_length_bytes must be within the appropriate range.")

    # Validate the number of payload length bytes before calculation.
    check_number_of_payload_length_bytes()

    # Calculate the maximum number of payload bytes.
    number_of_payload_length_bits = 8 * number_of_payload_length_bytes
    max_number_of_payload_bytes = 2 ** number_of_payload_length_bits - 1
    return max_number_of_payload_bytes  # type: ignore
