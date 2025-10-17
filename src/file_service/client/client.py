import sys
from . import networking


def main() -> None:
    server_host = sys.argv[1]
    server_port = int(sys.argv[2])
    networking.run_client(server_host, server_port)


if __name__ == "__main__":
    main()