import sys

DEBUG = False

# NOTE:
# I could validate the format or type of command-line arguments here, but I will not, because the brief did not specify
# that this was necessary.


def get_port() -> int:
    """
    Retrieve the port number from the command-line arguments.
    """
    # Convert the string input from the command line to an integer.
    port = int(sys.argv[1])
    if DEBUG:
        print("DEBUG: Port is:", port)
    return port
