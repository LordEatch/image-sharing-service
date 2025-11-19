from file_service.client.networking import run_client
from file_service.client.client_io import get_server_host, get_server_port


def main() -> None:
    """Start the client and connect to the specified server."""
    run_client(get_server_host(), get_server_port())


if __name__ == "__main__":
    main()
