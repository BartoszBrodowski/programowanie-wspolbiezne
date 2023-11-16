import os
import sys


def main():
    if len(sys.argv) != 2:
        print("Usage: python client.py <ID>")
        return

    # Get record id
    client_id = int(sys.argv[1])

    # Create a unique client FIFO queue
    client_fifo = f"client_fifo_{client_id}"
    os.mkfifo(client_fifo)

    # Send a request to the server
    server_fifo = "server_fifo"
    request = f"{client_id} {client_fifo}"
    with open(server_fifo, "w") as fifo:
        fifo.write(request)

    # Open the client's FIFO queue for reading the response
    with open(client_fifo, "r") as fifo:
        response = fifo.read()
        print(f"Response: {response}")

    os.remove(client_fifo)

if __name__ == "__main__":
    main()
