import socket


def play_round(player_choices):
    cases = {
        'paper': 'rock',
        'rock': 'scissors',
        'scissors': 'paper'
    }
    (p1, c1), (p2, c2) = player_choices
    if c1 == c2:
        return 'Draw'
    else:
        if cases[c1] == c2:
            return p1
        else:
            return p2


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('127.0.0.1', 12345)
    server_socket.bind(server_address)

    print('Server running at {}:{}'.format(*server_address))

    players = {}

    while True:
        data, client_address = server_socket.recvfrom(1024)
        message = data.decode('utf-8')
        player, choice = message.split(':')

        if choice.lower() == 'end':
            # Gracz chce zakończyć grę
            # Usunięcie gracza z listy aktywnych graczy
            players.pop(client_address, None)
            if not players:
                print('Reseting score')
            continue

        # Dodanie gracza do listy aktywnych graczy i zapisanie jego wyboru
        players[client_address] = (player, choice)
        print('Player {} chose {}'.format(player, choice))

        if len(players) == 2:
            # Oba wybory zostały odebrane, można rozegrać rundę
            result = play_round(list(players.values()))
            print('Player that won: {}'.format(result))

            # Wysłanie wyników obu graczom
            for addr, choice in players.items():
                response = 'Player that won: {}, chose: {}'.format(result, choice)
                server_socket.sendto(response.encode('utf-8'), addr)

            players.clear()


if __name__ == '__main__':
    start_server()
