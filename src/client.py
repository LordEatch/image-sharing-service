import socket

SERVER_IP_ADDRESS = "127.0.0.1"
SERVER_PORT = 1234

# NOTE
# You don’t specify a client port because the OS auto-assigns an ephemeral one to bind to the socket (49152-65535).
# The TCP handshake automatically communicates that port to the server.
# The server replies to that port as part of the established connection.
# You can manually bind to a port if you need full control (rare outside specialized networking scenarios).
# Servers need to define a port so that clients can connect to them.

# Create a TCP socket (SOCK_STREAM) that uses IPv4 (AF_INET).
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
with my_socket:
    # Connect to the server with IP address 127.0.0.1 on port 1234.
    my_socket.connect((SERVER_IP_ADDRESS, SERVER_PORT))
    # Now the client can send and receive data to the server.
    message = "Would you like me to show you a clean pattern that logs both normal exits and exceptions from a with block, while keeping the code readable (like for a socket or file handler)?"
    encoded_message = message.encode("utf-8")
    my_socket.sendall(encoded_message)
    print("Send the following message to the server: " + message)
print("Client finished.")