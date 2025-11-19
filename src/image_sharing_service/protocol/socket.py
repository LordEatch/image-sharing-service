from typing import Any, Callable, Literal
import pickle

# Message protocol constants
_PAYLOAD_SIZE_BYTES_COUNT = 4  # Number of prefix bytes describing payload size
_ENDIANNESS: Literal["big", "little"] = "big"


def get_max_payload_size(size_bytes_count: int = _PAYLOAD_SIZE_BYTES_COUNT) -> int:
    """Return the maximum possible payload size for the given byte count."""
    size: int = 2 ** (8 * size_bytes_count) - 1
    return size


def get_payload_size(payload: Any) -> int:
    """Return the number of bytes used to encode a payload."""
    data = pickle.dumps(payload)
    return len(data)


def frame_message(payload: Any) -> bytes:
    """Wrap a pickled payload with its length prefix."""
    data = pickle.dumps(payload)
    size = len(data)
    header = size.to_bytes(_PAYLOAD_SIZE_BYTES_COUNT, _ENDIANNESS)
    return header + data


def unframe_message(receive_data_from_sock_fn: Callable[[int], bytes]) -> Any:
    """Receive and unpickle a framed message from a socket."""
    header = receive_data_from_sock_fn(_PAYLOAD_SIZE_BYTES_COUNT)
    size = int.from_bytes(header, _ENDIANNESS)
    data = receive_data_from_sock_fn(size)
    payload = pickle.loads(data)
    return payload


def _validate_payload_size_bytes_count(count: int) -> None:
    """Ensure the byte count for payload size is within the valid range."""
    _MIN_COUNT = 1
    _MAX_COUNT = 8

    if not _MIN_COUNT <= count <= _MAX_COUNT:
        raise ValueError(
            f"Number of payload size bytes must be between {_MIN_COUNT} and {_MAX_COUNT}."
        )


# Validate configuration at import time
_validate_payload_size_bytes_count(_PAYLOAD_SIZE_BYTES_COUNT)
