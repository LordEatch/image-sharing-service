import sys

DEBUG = False

# NOTE:
# I could validate the format or type of command-line arguments here, but I will not, because the brief did not specify
# that such validation was required.


def get_server_host() -> str:
    """
    Retrieve the server host from the command-line arguments.
    """
    server_host = sys.argv[1]
    if DEBUG:
        print("DEBUG: Server host is:", server_host)
    return server_host


def get_server_port() -> int:
    """
    Retrieve the server port from the command-line arguments.
    """
    # Convert the string input from the command line to an integer.
    server_port = int(sys.argv[2])
    if DEBUG:
        print("DEBUG: Server port is:", server_port)
    return server_port
