from socket import socket, AF_INET, SOCK_STREAM
from . import networking


def main() -> None:
    networking.run_client()


if __name__ == "__main__":
    main()