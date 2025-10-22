import os

def download_file(filename: str, file_binary: bytes) -> None:
    filepath = os.path.join(os.getcwd(), filename)
    with open(filepath, "xb") as file:
        file.write(file_binary)

def get_file_binary(filepath: str) -> bytes:
    with open(filepath, "rb") as file:
        return file.read()