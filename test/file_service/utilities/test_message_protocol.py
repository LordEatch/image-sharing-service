import unittest
from src.file_service.utilities.message_protocol import get_max_number_of_payload_bytes

# NOTE
# I am only testing functions with their expected datatype. The main goal of unit testing is for correct behaviour. The only exception will be functions involving user input (if I remember).

class TestGetMaxNumberOfPayloadBytes(unittest.TestCase):
    def test_get_max_number_of_payload_bytes(self) -> None:
        self.assertEqual(get_max_number_of_payload_bytes(1), 255)
        self.assertEqual(get_max_number_of_payload_bytes(2), 65535)
        self.assertEqual(get_max_number_of_payload_bytes(4), 4294967295)
        self.assertEqual(get_max_number_of_payload_bytes(8), 18446744073709551615)
        self.assertRaises(ValueError, get_max_number_of_payload_bytes, -1)
        self.assertRaises(ValueError, get_max_number_of_payload_bytes, 0)
        self.assertRaises(ValueError, get_max_number_of_payload_bytes, 9)