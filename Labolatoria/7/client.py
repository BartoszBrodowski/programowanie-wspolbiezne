import socket
import time


def start_client(player_name):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('127.0.0.1', 12345)

    print("Player name: " + player_name)

    try:
        while True:
            choice = input(
                'Choose paper, rock or scissors ("end" to end the game): ')
            to_send = player_name + ":" + choice
            client_socket.sendto(to_send.encode('utf-8'), server_address)

            if choice.lower() == 'end':
                break

            data, _ = client_socket.recvfrom(1024)
            message = data.decode('utf-8')
            print(message)

    finally:
        client_socket.close()


if __name__ == '__main__':
    player_name = "Gracz" + str(time.time())[-3:]
    start_client(player_name)
