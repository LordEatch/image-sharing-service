import socket

IP_ADDRESS = "127.0.0.1"
PORT = 1234

def main() -> None:
    # Create a TCP socket (SOCK_STREAM) that uses IPv4 (AF_INET).
    listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Use listening_socket and close it after use.
    with listening_socket:
        # Bind the socket to the server's IP address and port. Now the server is reachable through this address and port.
        listening_socket.bind((IP_ADDRESS, PORT))
        # Mark this socket as a *listening socket*. This is a socket that can accept client connections.
        listening_socket.listen()
        print(f"Server running on IP address {IP_ADDRESS} and port {PORT}.")
        # When a client connects, accept() returns a *new socket*, and the address of the client. This client_socket is used to communicate with the client.
        client_socket, client_address = listening_socket.accept()
        # Use client_socket and close it after use.
        with client_socket:
            print(f"{client_address} has connected.")
            # Now the server can send and receive data to and from the client.
            data = client_socket.recv(1024)
            print(data.decode("utf-8"))
        print(f"The connection with {client_address} has been closed.")
    print("Server finished.")

if __name__ == "__main__":
    main()