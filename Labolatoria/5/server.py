import sysv_ipc
import time

input_queue_key = 11
output_queue_key = 12

try:
    input_queue = sysv_ipc.MessageQueue(input_queue_key, sysv_ipc.IPC_CREAT | 0o600)
    output_queue = sysv_ipc.MessageQueue(output_queue_key, sysv_ipc.IPC_CREAT | 0o600)
except sysv_ipc.ExistentialError:
    print("Kolejki już istnieją.")

dictionary = {
    "kot": "cat",
    "pies": "dog",
    "dom": "house",
    "samochód": "car",
}

while True:
    message, type = input_queue.receive(type=0)
    time.sleep(3)
    word = message.strip().decode()

    if word in dictionary:
        translation = dictionary[word]
    else:
        translation = "Nie znam takiego słowa."

    output_queue.send(translation.encode(), True, type)