import os
from file_service.utilities.debug import print_debug


def save_local_file(filename: str, file: bytes) -> None:
    """Save a file to the current working directory. Raise FileExistsError if it already exists."""
    filepath = _full_path(filename)
    with open(filepath, "xb") as f:
        f.write(file)
    print_debug(f"File saved successfully.\n\tPath: {filepath}")


def get_local_file(filename: str) -> bytes:
    """Retrieve a file from the current working directory. Raise FileNotFoundError if the file is missing."""
    file = get_file(_full_path(filename))
    print_debug(f"File retrieved successfully.\n\tPath: {_full_path(filename)}")
    return file


def get_local_list() -> list[str]:
    return os.listdir(os.getcwd())


def get_image(filepath: str) -> bytes:
    """
    Retrieve an image file (.jpg, .jpeg, .png) from the current working directory.
    Raises ValueError if the file is not one of the allowed image types.
    """
    _VALID_EXTENSIONS = {".jpg", ".jpeg", ".png"}

    _, extension = os.path.splitext(filepath)
    if extension.lower() not in _VALID_EXTENSIONS:
        raise ValueError(f"Invalid image type '{extension}'. Allowed types are: {', '.join(_VALID_EXTENSIONS)}.")
    return get_file(filepath)


def get_file(filepath: str) -> bytes:
    """Read a file into bytes. Raise FileNotFoundError if the file is missing."""
    with open(filepath, "rb") as f:
        file = f.read()
    print_debug(f"File read successfully.\n\tPath: {filepath}")
    return file


def _full_path(filename: str) -> str:
    return os.path.join(os.getcwd(), filename)
