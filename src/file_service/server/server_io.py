import sys

from file_service.utilities.debug import print_debug


# Erroneous user inputs are not caught because the brief did not specify that such validation was required.

def get_port() -> int:
    """Retrieve the port number from the command-line arguments."""
    port = int(sys.argv[1])
    print_debug(f"User inputted port: {port}.")
    return port
