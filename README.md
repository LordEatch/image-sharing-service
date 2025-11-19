# Image Sharing Service

## Overview
This package implements a simple **client–server file transfer system** over TCP sockets in Python. It enables clients to **upload (PUT)**, **download (GET)**, and **list (LIST)** image files stored on the server. Only files in **JPEG, JPG, or PNG** formats are supported.

The design focuses on:
- Reliable, structured communication using a custom **application-level protocol**.
- **Binary-safe** file transfer.
- Clear separation between **transport (socket)** and **application (message)** layers.
- **Extensibility** for new commands or features.

## Features
- **PUT** — upload image files to the server (rejects duplicates or empty files).  
- **GET** — download existing image files from the server.  
- **LIST** — retrieve a list of all stored files on the server.  
- **Structured messages** with error reporting and clear status codes.  
- Modular and maintainable architecture.  

## Protocol design

### Message structure
All communication between client and server uses **pickled Python dictionaries** framed with a **4-byte size header**.

Each message (“payload”) includes:
| Key | Description |
|-----|--------------|
| `COMMAND` | Operation type (`PUT`, `GET`, `LIST`). |
| `STATUS` | Current stage or result (`REQUEST`, `OK`, `ERROR`). |
| `DETAILS` | Optional text describing results or errors. |
| `FILENAME` | Name of the file being transferred (if applicable). |
| `FILE_DATA` | Raw binary data of the file (only for transfers). |

All messages are serialized using `pickle` and prefixed with a 4-byte integer indicating the payload size in bytes.

Example:
<payload_byte_count: 125>
<payload: {
"COMMAND": "PUT",
"STATUS": "REQUEST",
"DETAILS": None,
"FILENAME": "image.png",
"FILE_DATA": b'\x89PNG...'
}>

## Command workflows

### PUT
1. Client verifies the file exists and is in `.jpg`, `.jpeg`, or `.png` format.  
2. Sends `REQUEST` payload with file name and binary data.  
3. Server checks for duplicates or invalid data.  
4. On success, saves file and replies with `STATUS = OK`.  
5. On failure, replies with `STATUS = ERROR` and a descriptive message.

### GET
1. Client sends `REQUEST` with filename to download.  
2. Server looks up the file:  
   - If found → responds with `STATUS = OK` and file data.  
   - If not found → responds with `STATUS = ERROR` and explanation.  

### LIST
1. Client sends `REQUEST` with `COMMAND = LIST`.  
2. Server compiles list of stored filenames.  
3. Returns it in the `DETAILS` field of the response.  
4. If directory is empty, returns an appropriate message.

## Design decisions

### Pickled payloads
Using Python’s `pickle` module allows flexible serialization of mixed data types (strings, bytes, dicts) without custom parsing logic.

### Framed messages
Prefixing each payload with its size ensures **robust message boundaries** across the TCP stream and prevents partial reads.

### Error handling
All failures (missing files, duplicates, format errors, connection issues) produce structured `ERROR` messages with explanations.

### Binary file support
Files are always handled in binary mode (`rb` / `wb`) to ensure accurate image transfer.

### Extensibility
New commands can easily be added by extending the `COMMAND` field and implementing handlers on both client and server.

## Package structure

image_sharing_service/  
├── init.py  
├── client.py  
├── server.py  
├── protocol/  
│ ├── init.py  
│ ├── socket.py # Low-level TCP read/write  
│ └── message.py # Framing and payload parsing  
└── utilities/  
├── init.py  
├── socket_utils.py # Sending data over sockets  
└── message_utils.py # Sending/receiving structured payloads  

## Example interaction

Client:  
COMMAND: PUT  
STATUS: REQUEST  
FILENAME: "cat.jpg"  
FILE_DATA: <binary>  

Server:  
COMMAND: PUT  
STATUS: OK  
DETAILS: None  
FILENAME: "cat.jpg"  
FILE_DATA: None  

...or on error:  
COMMAND: PUT  
STATUS: ERROR  
DETAILS: "File 'cat.jpg' already exists on server"  
FILENAME: "cat.jpg"  
FILE_DATA: None  

## Requirements

- Python 3.10+.
- Standard library only (no external dependencies).
- Compatible with Windows, macOS, and Linux.