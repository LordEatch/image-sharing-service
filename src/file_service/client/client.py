from .networking import run_client
from .client_io import get_server_host, get_server_port


def main() -> None:
    run_client(get_server_host(), get_server_port())


if __name__ == "__main__":
    main()