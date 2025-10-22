import unittest
from src.file_service.utilities.message_protocol import _validate_payload, _get_max_payload_size


class TestValidatePayload(unittest.TestCase):

    def test_valid_payload(self) -> None:
        """Test that a valid payload passes all validations."""
        payload = {
            "command": "put",
            "status": "success",
            "filename": "test.txt",
            "file_data": b"file content"
        }
        # Should not raise any exceptions.
        _validate_payload(payload)

    def test_missing_required_keys(self) -> None:
        """Test that missing keys raise KeyError."""
        payload = {
            "command": "put",
            "status": "success"
            # Missing filename and file_data.
        }
        self.assertRaises(KeyError, _validate_payload, payload)

    def test_invalid_command_type(self) -> None:
        """Test that a non-string command raises TypeError."""
        payload = {
            "command": 123,  # Should be string.
            "status": "success",
            "filename": "test.txt",
            "file_data": b"content"
        }
        self.assertRaises(TypeError, _validate_payload, payload)

    def test_invalid_status_type(self) -> None:
        """Test that non-string status raises TypeError."""
        payload = {
            "command": "put",
            "status": 200,  # Should be string.
            "filename": "test.txt",
            "file_data": b"content"
        }
        self.assertRaises(TypeError, _validate_payload, payload)

    def test_valid_none_filename(self) -> None:
        """Test that None is acceptable for filename."""
        payload = {
            "command": "list",
            "status": "success",
            "filename": None,  # Should be allowed.
            "file_data": None
        }
        # Should not raise any exceptions.
        _validate_payload(payload)

    def test_invalid_filename_type(self) -> None:
        """Test that non-string/non-None filename raises TypeError."""
        payload = {
            "command": "put",
            "status": "success",
            "filename": 123,  # Should be string or None.
            "file_data": b"content"
        }
        self.assertRaises(TypeError, _validate_payload, payload)

    def test_invalid_file_data_type(self) -> None:
        """Test that non-bytes/non-None file_data raises TypeError."""
        payload = {
            "command": "put",
            "status": "success",
            "filename": "test.txt",
            "file_data": "not bytes"  # Should be bytes or None.
        }
        self.assertRaises(TypeError, _validate_payload, payload)

    def test_payload_too_large(self) -> None:
        """Test that oversized payload raises ValueError."""
        # Create a payload with large file data to exceed the size limit.
        large_data = b"x" * (1024 * 1024 * 10)  # 10MB of data.
        payload = {
            "command": "put",
            "status": "success",
            "filename": "large_file.txt",
            "file_data": large_data
        }
        self.assertRaises(ValueError, _validate_payload, payload)

    def test_valid_empty_payload(self) -> None:
        """Test that payload with empty strings and None values is valid."""
        payload = {
            "command": "",
            "status": "",
            "filename": "",
            "file_data": b""
        }
        # Should not raise any exceptions.
        _validate_payload(payload)

    def test_valid_none_file_data(self) -> None:
        """Test that None is acceptable for file_data."""
        payload = {
            "command": "get",
            "status": "request",
            "filename": "test.txt",
            "file_data": None  # Should be allowed.
        }
        # Should not raise any exceptions.
        _validate_payload(payload)


class TestGetMaxPayloadSize(unittest.TestCase):

    def test_all(self) -> None:
        self.assertEqual(_get_max_payload_size(1), 255)
        self.assertEqual(_get_max_payload_size(2), 65535)
        self.assertEqual(_get_max_payload_size(4), 4294967295)
        self.assertEqual(_get_max_payload_size(8), 18446744073709551615)

        # These should all exceed the limit of allocated bytes.
        self.assertRaises(ValueError, _get_max_payload_size, -1)
        self.assertRaises(ValueError, _get_max_payload_size, 0)
        self.assertRaises(ValueError, _get_max_payload_size, 9)


if __name__ == '__main__':
    unittest.main()