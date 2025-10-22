from typing import Any, Callable, Literal
import pickle

# Message protocol constants.
_PAYLOAD_SIZE_BYTES_COUNT = 2  # Number of prefixing bytes that describe the size of the payload.
_ENDIANNESS: Literal["big", "little"] = "big"

# Payload dictionary constants.
# Keys.
COMMAND_KEY = "command"
STATUS_KEY = "status"
FILENAME_KEY = "filename"
FILE_DATA_KEY = "file_data"
# Command values.
PUT_VAL = "put"
GET_VAL = "get"
LIST_VAL = "list"
# Status values.
REQUEST_VAL = "request"
OK_VAL = "ok"
ERROR_VAL = "error"


def frame_message(payload: dict[str, Any]) -> bytes:
    """Wrap a pickled payload with its length prefix. Validate the payload before framing."""
    data = pickle.dumps(payload)
    size = len(data)
    _validate_payload(payload)
    header = size.to_bytes(_PAYLOAD_SIZE_BYTES_COUNT, _ENDIANNESS)
    return header + data


def unframe_message(recv_fn: Callable[[int], bytes]) -> dict[str, Any]:
    """Receive a framed message from a socket and return the unpickled payload. Validate the payload after unframing."""
    def receive_payload_size() -> int:
        return int.from_bytes(recv_fn(_PAYLOAD_SIZE_BYTES_COUNT), _ENDIANNESS)

    def receive_payload(size: int) -> dict[str, Any]:
        return pickle.loads(recv_fn(size))  # type: ignore

    payload: dict[str, Any] = receive_payload(receive_payload_size())
    _validate_payload(payload)
    return payload


def _validate_payload(payload: dict[str, Any]) -> None:
    def _validate_keys() -> None:
        """Raise an exception if any of the required keys are missing."""
        required_keys = {"command", "status", "filename", "file_data"}
        missing_keys = required_keys - payload.keys()
        if missing_keys:
            raise KeyError(f"Missing required keys: {missing_keys}")

    def _validate_value_types() -> None:
        """Validate that payload values have the correct types."""
        if not isinstance(payload[COMMAND_KEY], str):
            raise TypeError("Command must be a string.")
        if not isinstance(payload[STATUS_KEY], str):
            raise TypeError("Status must be a string.")
        if not isinstance(payload[FILENAME_KEY], (str, type(None))):
            raise TypeError("Filename must be str or None.")
        if not isinstance(payload[FILE_DATA_KEY], (bytes, type(None))):
            raise TypeError("File data must be bytes or None.")

    def _validate_size() -> None:
        """Make sure a payload (any python object) is not too big."""
        def get_size() -> int:
            data = pickle.dumps(payload)
            size = len(data)
            return size

        max_size = _get_max_payload_size(_PAYLOAD_SIZE_BYTES_COUNT)
        if get_size() > max_size:
            raise ValueError(f"Payload too large (max {max_size} bytes).")

    _validate_keys()
    _validate_value_types()
    _validate_size()

def _get_max_payload_size(size_bytes_count: int) -> int:
    """Get the maximum possible payload size given size_bytes_count."""
    def validate_payload_size_bytes_count() -> None:
        """Make sure size_bytes_count is within the allowed range."""
        _MIN_PAYLOAD_SIZE_BYTES_COUNT = 1
        _MAX_PAYLOAD_SIZE_BYTES_COUNT = 8
        if not _MIN_PAYLOAD_SIZE_BYTES_COUNT <= size_bytes_count <= _MAX_PAYLOAD_SIZE_BYTES_COUNT:
            raise ValueError(f"Number of payload size bytes must be between {_MIN_PAYLOAD_SIZE_BYTES_COUNT} and {_MAX_PAYLOAD_SIZE_BYTES_COUNT}.")

    validate_payload_size_bytes_count()
    max_size: int = 2 ** (8 * size_bytes_count) - 1
    return max_size