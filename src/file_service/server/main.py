from file_service.server.networking import run_server
from file_service.server.server_io import get_port


def main() -> None:
    """Start the server on the selected port."""
    run_server(get_port())


if __name__ == "__main__":
    main()
