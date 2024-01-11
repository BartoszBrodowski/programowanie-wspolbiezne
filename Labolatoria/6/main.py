import sysv_ipc
from constants import KLUCZ, POSSIBLE_CARDS, NULL_CHAR

sem1 = None
sem2 = None
mem1 = None
mem2 = None

second_player = False

try:
    sem1 = sysv_ipc.Semaphore(KLUCZ, sysv_ipc.IPC_CREX,0o700,0)
    sem2 = sysv_ipc.Semaphore(KLUCZ+1, sysv_ipc.IPC_CREX,0o700,1)
    mem1 = sysv_ipc.SharedMemory(KLUCZ, sysv_ipc.IPC_CREX)
    mem2 = sysv_ipc.SharedMemory(KLUCZ + 1, sysv_ipc.IPC_CREX)
except sysv_ipc.ExistentialError:
    print("You're 2nd player")
    second_player = True
    sem1 = sysv_ipc.Semaphore(KLUCZ + 1)
    sem2 = sysv_ipc.Semaphore(KLUCZ)
    mem1 = sysv_ipc.SharedMemory(KLUCZ + 1)
    mem2 = sysv_ipc.SharedMemory(KLUCZ)

def pisz(mem, card):
    card = card + NULL_CHAR
    card = card.encode()
    mem.write(card)

def czytaj(players_card, mem):
    s = mem.read()
    if (second_player):
        mem.write(NULL_CHAR)
    s = s.decode()
    i = s.find(NULL_CHAR)
    if i != -1:
        s = s[:i]
    if len(s.strip()) != 0:
        if s == players_card:
            print("Wygrywa gracz 2")
        else:
            print("Wygrywa gracz 1")

def read_card():
    player_info = 'Choose your card (1st player): ' if second_player == False else 'Choose your card (2nd player): '
    card = input(player_info).lower()
    if card not in POSSIBLE_CARDS:
        print('Wrong input, choose a,b or c')
        read_card()
    
    return card

for i in range(0, 3):
    sem2.acquire()
    card = read_card()
    pisz(mem1, card)
    sem1.release()
    if second_player == False:
        sem2.acquire()
    else:
        sem1.release()
    card_from_memory = czytaj(card, mem2)

if second_player == True:
    mem1.remove()
    mem2.remove()
    sem1.remove()
    sem2.remove()