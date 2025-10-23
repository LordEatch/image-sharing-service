from typing import Any

from file_service.protocol import socket as socket_protocol

# Keys
COMMAND_KEY = "COMMAND"
STATUS_KEY = "STATUS"
DETAILS_KEY = "DETAILS"
FILENAME_KEY = "FILENAME"
FILE_DATA_KEY = "FILE_DATA"

# Command values
PUT_VAL = "PUT"
GET_VAL = "GET"
LIST_VAL = "LIST"

# Status values
REQUEST_VAL = "REQUEST"
OK_VAL = "OK"
ERROR_VAL = "ERROR"


class SizeError(Exception):
    """Raised when a payload exceeds the maximum allowed size."""
    pass


class CommandError(Exception):
    """Raised when a command value is invalid."""
    pass


def construct_payload(
    command: str | None = None,
    status: str | None = None,
    details: str | None = None,
    filename: str | None = None,
    file_data: bytes | None = None,
) -> dict[str, Any]:
    """Construct a payload dictionary with all required keys."""
    payload = {
        COMMAND_KEY: command,
        FILENAME_KEY: filename,
        DETAILS_KEY: details,
        STATUS_KEY: status,
        FILE_DATA_KEY: file_data,
    }
    validate_payload(payload)
    return payload


def validate_payload(payload: dict[str, Any]) -> None:
    """Validate a payload and raise an appropriate error if invalid."""

    def validate_keys() -> None:
        """Ensure all required keys are present."""
        required = {
            COMMAND_KEY,
            STATUS_KEY,
            DETAILS_KEY,
            FILENAME_KEY,
            FILE_DATA_KEY,
        }
        missing = required - payload.keys()
        if missing:
            raise KeyError(f"Missing required keys: {missing}.")

    def validate_value_types() -> None:
        """Ensure all values are of valid types."""
        if not isinstance(payload[COMMAND_KEY], (str, type(None))):
            raise TypeError("Command must be a string or None.")
        if not isinstance(payload[STATUS_KEY], (str, type(None))):
            raise TypeError("Status must be a string or None.")
        if not isinstance(payload[DETAILS_KEY], (str, type(None))):
            raise TypeError("Details must be a string or None.")
        if not isinstance(payload[FILENAME_KEY], (str, type(None))):
            raise TypeError("Filename must be a string or None.")
        if not isinstance(payload[FILE_DATA_KEY], (bytes, type(None))):
            raise TypeError("File data must be bytes or None.")

    def validate_size() -> None:
        """Ensure the payload does not exceed the size limit."""
        size = socket_protocol.get_payload_size(payload)
        max_size = socket_protocol.get_max_payload_size()
        if size > max_size:
            raise SizeError(f"Payload too large (max {max_size} bytes).")

    def validate_command() -> None:
        """Ensure the command is valid."""
        if payload[COMMAND_KEY] not in [PUT_VAL, GET_VAL, LIST_VAL]:
            raise CommandError(f"Invalid command: {payload[COMMAND_KEY]}.")

    validate_keys()
    validate_value_types()
    validate_size()
    validate_command()
