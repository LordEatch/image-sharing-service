from typing import Dict
import pickle  # pickle is used to serialize python objects for binary transmission.

NUMBER_OF_PREFIX_BYTES = 2


def compose_message(message: Dict[str, str]) -> bytes:
    """Put a message into a datagram for transmission."""

    # Calculate the maximum number of bytes that can be stored in the message given the number of prefix bytes.
    number_of_prefix_bits = 8 * NUMBER_OF_PREFIX_BYTES
    message_max_number_of_bytes = 2 ** number_of_prefix_bits - 1

    message_bytes = pickle.dumps(message)
    message_number_of_bytes = len(message_bytes)
    if message_number_of_bytes > message_max_number_of_bytes:
        raise ValueError(f"Message too large. Max size is {message_max_number_of_bytes} bytes.")
    message_prefix = message_number_of_bytes.to_bytes(NUMBER_OF_PREFIX_BYTES, "big")
    full_message_bytes = message_prefix + message_bytes
    return full_message_bytes


# def receive_message(message_bytes: bytes) -> Dict[str, str]:
#     message_number_of_bytes = int.from_bytes(message_bytes[:NUMBER_OF_PREFIX_BYTES], "big")
#     message_bytes = message_bytes[NUMBER_OF_PREFIX_BYTES:]
#     message = pickle.loads(message_bytes)
#     return message

compose_message({"message": "Hello, world!"})
