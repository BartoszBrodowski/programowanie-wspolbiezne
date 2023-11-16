import os
import time
import signal
import sys
import threading
import atexit

def handle_sighup(signum, frame):
    print("Received SIGHUP signal. Server continues running.")

def handle_sigterm(signum, frame):
    print("Received SIGTERM signal. Server continues running.")

def handle_sigusr1(signum, frame):
    print("Received SIGUSR1 signal. Server is terminating.")
    sys.exit(0)

def client_handler(client_id, client_fifo):
    response = database.get(client_id, "Nie ma")

    time.sleep(2)

    with open(client_fifo, "w") as fifo:
        fifo.write(response)

def cleanup():
    if os.path.exists(server_fifo):
        os.remove(server_fifo)

server_pid = os.getpid()
print(f"Server PID: {server_pid}")

# Set up signal handlers
signal.signal(signal.SIGHUP, handle_sighup)
signal.signal(signal.SIGTERM, handle_sigterm)
signal.signal(signal.SIGUSR1, handle_sigusr1)

# DB
database = {1: "Smith", 2: "Johnson", 3: "Brown"}

# Create a FIFO queue for the server
server_fifo = "server_fifo"
os.mkfifo(server_fifo)
# Delete server fifo
atexit.register(cleanup)

while True:
    with open(server_fifo, "r") as fifo:
        data = fifo.read()
        if data:
            parts = data.split()
            client_id = int(parts[0])
            client_fifo = parts[1]

            client_thread = threading.Thread(target=client_handler, args=(client_id, client_fifo))
            client_thread.start()
