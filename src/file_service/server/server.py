from .networking import run_server
from .server_io import get_port


def main() -> None:
    run_server(get_port())


if __name__ == "__main__":
    main()
