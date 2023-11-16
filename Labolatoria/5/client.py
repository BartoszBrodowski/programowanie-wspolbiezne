import sysv_ipc
import os

input_queue_key = 11
output_queue_key = 12

input_queue = sysv_ipc.MessageQueue(input_queue_key)
output_queue = sysv_ipc.MessageQueue(output_queue_key)

word = "kot"
client_pid = os.getpid()

input_queue.send(word.encode(), True, client_pid) # add type

response, _ = output_queue.receive() # add type
translation = response.strip().decode()

print(f"Tłumaczenie słowa '{word}': {translation}")
