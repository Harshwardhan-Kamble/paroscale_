import socket
import threading

HOST = "0.0.0.0"
PORT = 8080

indexed_packages = set()
dependencies = {}

lock = threading.Lock()
request_count = 0

def process_message(message):
    global request_count

    request_count += 1

    if request_count % 100 == 0:
        print(f"Processed {request_count} requests")

    parts = message.split("|")

    if len(parts) != 3:
        return "ERROR\n"

    command = parts[0].strip()
    package = parts[1].strip()
    deps_field = parts[2].strip()

    if command not in {"INDEX", "REMOVE", "QUERY"}:
        return "ERROR\n"

    if not package:
        return "ERROR\n"

    with lock:

        if command == "REMOVE":
            indexed_packages.discard(package)
            return "OK\n"

        elif command == "QUERY":
            if package in indexed_packages:
                return "OK\n"
            return "FAIL\n"

        elif command == "INDEX":

            dep_set = set()

            if deps_field:
                dep_set = {
                    dep.strip()
                    for dep in deps_field.split(",")
                    if dep.strip()
                }

            dependencies[package] = dep_set

            indexed_packages.add(package)

            print("Dependencies:", dependencies)

            return "OK\n"

        return "ERROR\n"


def handle_client(conn, addr):
    buffer = ""

    try:
        while True:

            try:
                data = conn.recv(4096)
            except ConnectionResetError:
                break

            if not data:
                break

            buffer += data.decode()

            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)

                response = process_message(line.strip())

                conn.sendall(response.encode())

    finally:
        conn.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))
server.listen()

print(f"Listening on {PORT}")

while True:
    conn, addr = server.accept()

    threading.Thread(
        target=handle_client,
        args=(conn, addr),
        daemon=True
    ).start()
