import sys
from ..utilities.debug import print_debug


# Erroneous user inputs are not caught because the brief did not specify that such validation was required.

def get_port() -> int:
    """
    Retrieve the port number from the command-line arguments.
    """
    # Convert the string input from the command line to an integer.
    port = int(sys.argv[1])
    print_debug(f"User inputted port: {port}.")
    return port
