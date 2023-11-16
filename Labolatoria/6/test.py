import sysv_ipc
import time

semaphore_key= 32
memory_key = 311
NULL_CHAR = '\0'
possible_cards = ['a', 'b', 'c']

def run():
    try:
        mem = sysv_ipc.SharedMemory(memory_key, sysv_ipc.IPC_CREX)
        sem = sysv_ipc.Semaphore(semaphore_key, sysv_ipc.IPC_CREX,0o700,1)
        chosen_card = input('Choose your card (1st player): ').lower()
        if chosen_card not in possible_cards:
            return False
        pierwszy = True
        mem.write((chosen_card + NULL_CHAR).encode())
        mem.read()
    except sysv_ipc.ExistentialError:
        mem = sysv_ipc.SharedMemory(memory_key)
        sem = sysv_ipc.Semaphore(semaphore_key)
        chosen_card = input('Choose your card (2nd player): ').lower()
        pierwszy=False
        mem.write((chosen_card + NULL_CHAR).encode())
        time.sleep(0.1)
        # Only the second player deletes it
        sem.remove()
        mem.remove()
    if pierwszy:
        print('jestem pierwszy')
        time.sleep(5)
    else:
        print('jestem drugi')
    
if __name__ == '__main__':
    run()