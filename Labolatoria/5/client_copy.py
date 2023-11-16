import sysv_ipc

input_queue_key = 11
output_queue_key = 12

input_queue = sysv_ipc.MessageQueue(input_queue_key)
output_queue = sysv_ipc.MessageQueue(output_queue_key)

word = "pies"

input_queue.send(word.encode())

response, _ = output_queue.receive()
translation = response.strip().decode()

print(f"Tłumaczenie słowa '{word}': {translation}")
