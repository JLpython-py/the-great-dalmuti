#! python3
# The_Great_Dalmuti_SERVER.py

import pickle
import random
import select
import socket
import sys
import threading

SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
LOCAL_HOSTNAME = socket.gethostname()
LOCAL_FQDN = socket.getfqdn()
IP_ADDRESS = socket.gethostbyname(LOCAL_HOSTNAME)
PORT = 2020
SERVER = (IP_ADDRESS, PORT)
SOCK.bind(SERVER)
SOCK.listen(8)

class GameData:
    ''' Basic game data for "The Great Dalmuti"
'''
    def __init__(self):
        self.card_images = (
            '1_1.jpg',
            '2_1.jpg', '2_2.jpg',
            '3_1.jpg', '3_2.jpg', '3_3.jpg',
            '4_1.jpg', '4_2.jpg', '4_3.jpg', '4_4.jpg',
            '5_1.jpg', '5_2.jpg', '5_3.jpg', '5_4.jpg', '5_5.jpg',
            '6_1.jpg', '6_2.jpg', '6_3.jpg', '6_4.jpg', '6_5.jpg',
            '6_6.jpg',
            '7_1.jpg', '7_2.jpg', '7_3.jpg', '7_4.jpg', '7_5.jpg',
            '7_6.jpg', '7_7.jpg',
            '8_1.jpg', '8_2.jpg', '8_3.jpg', '8_4.jpg', '8_5.jpg',
            '8_6.jpg', '8_7.jpg', '8_8.jpg',
            '9_1.jpg', '9_2.jpg', '9_3.jpg', '9_4.jpg', '9_5.jpg',
            '9_6.jpg', '9_7.jpg', '9_8.jpg', '9_9.jpg',
            '10_1.jpg', '10_2.jpg', '10_3.jpg', '10_4.jpg', '10_5.jpg',
            '10_6.jpg', '10_7.jpg', '10_8.jpg', '10_9.jpg', '10_10.jpg',
            '11_1.jpg', '11_2.jpg', '11_3.jpg', '11_4.jpg', '11_5.jpg',
            '11_6.jpg', '11_7.jpg', '11_8.jpg', '11_9.jpg', '11_10.jpg',
            '11_11.jpg',
            '12_1.jpg', '12_2.jpg', '12_3.jpg', '12_4.jpg', '12_5.jpg',
            '12_6.jpg', '12_7.jpg', '12_8.jpg', '12_9.jpg', '12_10.jpg',
            '12_11.jpg', '12_12.jpg',
            'J_1.jpg', 'J_2.jpg')
        self.card_rear = 'x_x.jpg'
        self.settings = {
            4: ('Great Dalmuti', 'Lesser Dalmuti',
                   'Lesser Peon', 'Greater Peon'),
            5: ('Great Dalmuti', 'Lesser Dalmuti',
                   'Merchant A',
                   'Lesser Peon', 'Greater Peon'),
            6: ('Great Dalmuti', 'Lesser Dalmuti',
                   'Merchant A', 'Merchant B',
                   'Lesser Peon', 'Greater Peon'),
            7: ('Great Dalmuti', 'Lesser Dalmuti',
                   'Merchant A', 'Merchant B', 'Merchant C',
                   'Lesser Peon', 'Greater Peon'),
            8: ('Great Dalmuti', 'Lesser Dalmuti',
                   'Merchant A', 'Merchant B', 'Merchant C', 'Merchant D',
                   'Lesser Peon', 'Greater Peon')}
        self.ranks = {
            'Jester': (
                'J_1.jpg', 'J_2.jpg'),
            'Great Dalmuti': (
                '1_1.jpg',),
            'Archbishop': (
                '2_1.jpg', '2_2.jpg'),
            'Earl Marshal': (
                '3_1.jpg', '3_2.jpg', '3_3.jpg'),
            'Baroness': (
                '4_1.jpg', '4_2.jpg', '4_3.jpg', '4_4.jpg'),
            'Abbess': (
                '5_1.jpg', '5_2.jpg', '5_3.jpg', '5_4.jpg', '5_5.jpg'),
            'Knight': (
                '6_1.jpg', '6_2.jpg', '6_3.jpg', '6_4.jpg', '6_5.jpg',
                '6_6.jpg'),
            'Seamstress': (
                '7_1.jpg', '7_2.jpg', '7_3.jpg', '7_4.jpg', '7_5.jpg',
                '7_6.jpg', '7_7.jpg'),
            'Mason': (
                '8_1.jpg', '8_2.jpg', '8_3.jpg', '8_4.jpg', '8_5.jpg',
                '8_6.jpg', '8_7.jpg', '8_8.jpg'),
            'Cook': (
                '8_1.jpg', '8_2.jpg', '8_3.jpg', '8_4.jpg', '8_5.jpg',
                '8_6.jpg', '8_7.jpg', '8_8.jpg'),
            'Shepherdress': (
                '10_1.jpg', '10_2.jpg', '10_3.jpg', '10_4.jpg', '10_5.jpg',
                '10_6.jpg', '10_7.jpg', '10_8.jpg', '10_9.jpg', '10_10.jpg'),
            'Stonecutter': (
                '11_1.jpg', '11_2.jpg', '11_3.jpg', '11_4.jpg', '11_5.jpg',
                '11_6.jpg', '11_7.jpg', '11_8.jpg', '11_9.jpg', '11_10.jpg',
                '11_11.jpg'),
            'Peasant': (
                '12_1.jpg', '12_2.jpg', '12_3.jpg', '12_4.jpg', '12_5.jpg',
                '12_6.jpg', '12_7.jpg', '12_8.jpg', '12_9.jpg', '12_10.jpg',
                '12_11.jpg', '12_12.jpg')}

class Network:
    def __init__(self):
        self.game_data = GameData()
        self.players = {}
        self.history = []
        self.turn = {
            'Quantity': 0,
            'Value': 0}

    def add_connection(self, player, conn, addr):
        self.new_player(player, conn, addr)
        print('Connection from {}'.format(player))
        self.players[player]['Connected'] = player in self.players
        self.players[player]['Status'] = False

    def terminate_connection(self, player):
        self.players[player]['Connected'] = False
        self.players[player]['Status'] = None
        print('Lost Connection with {}'.format(player),
              file=sys.stderr)
        self.history.append('Lost Connection with {}'.format(player))
        del self.players[player]

    def terminate_all(self):
        print('Ending Connections',
              file=sys.stderr)
        for player in Game.players:
            self.terminate_connection(player)
            print('Terminating Connection with {}'.format(player),
                  file=sys.stderr)
        print('Closing Socket',
              file=sys.stderr)
        SOCK.close()

    def new_player(self, player, conn, address):
        self.players.setdefault(
            player,
            {'Connection': conn,
             'Address': address})
        self.history.append(f'{player} Joined the Game')

    def player_status(self, player, status):
        if status != self.players[player]['Status']:
            event = '{} is Ready'.format(player) if status\
                    else '{} Canceled'.format(player)
            self.history.append(event)

class Screens:
    def __init__(self):
        self.network = Network()

    def home_screen(self):
        read_list = [SOCK]
        self.connections = []
        print('Searching for Connections')
        searching = True
        while searching:
            read, write, error = select.select(read_list, [], [])
            if SOCK in read:
                conn, addr = SOCK.accept()
                read_list.append(conn)
                print('Processing Connection Request')

                player = conn.recv(2048).decode('utf-8')
                self.network.add_connection(player, conn, addr)
                thread = threading.Thread(
                    target=self.waiting_room,
                    args=(player,))
                self.connections.append(thread)
                thread.start()

    def waiting_room(self, player):
        conn = self.network.players[player].get('Connection')
        active = True
        while active:
            active = not (
                all([self.network.players[p].get('Status')\
                     for p in self.network.players])
                and (4 <= len(self.network.players) <= 8)
                )
            try:
                status = pickle.loads(conn.recv(2048))
                print('Receiving {} Status({}) [{}]'.format(
                    player, status, sys.getsizeof(status)))
            except ConnectionResetError as e:
                status = None
                print(e, file=sys.stdout)
                self.network.history.append('{} Disconnected'.format(player))
                print('{} Disconnected'.format(player),
                      file=sys.stderr)
            if status is None:
                self.network.terminate_connection(player)
                break
            self.network.player_status(player, status)
            self.network.players[player]['Status'] = status

            update = self.network.history[-1]
            conn.sendall(pickle.dumps(update))
            print('Sending Game Update [{}]'.format(
                sys.getsizeof(update)))

            conn.sendall(pickle.dumps(active))
            print('Sending Game Status({}) [{}]'.format(
                active, sys.getsizeof(active)))

    def game_screen(self):
        conn = self.network.players[player].get('Connection')
        active = {
            'Screen': True,
            'Status': True,
            'Turn': False}
        while active['Screen']:
            active['Screen'] = Active.game_screen()

            try:
                active['Status'] = pickle.loads(conn.recv(2048))
                print('Receiving {} Status({}) [{}]'.format(
                    player, status, sys.getsizeof(status)))
            except ConnectionResetError as e:
                active['Status'] = None
                print(e, file=sys.stdout)
                Game.history.append('{} Disconnected'.format(player))
                print('{} Disconnected'.format(player),
                      file=sys.stderr)
            if status is None:
                Network.terminate_connection(player)
                break
            Process_Data.player_status(player, status)
            Game.players[player]['Status'] = status
            

            conn.sendall(pickle.dumps(active['Screen']))
            print('Sending Game Status({}) [{}]'.format(
                active, sys.getsizeof(active['Screen'])))

            active['Turn'] = Game.player[player]['Turn']
            conn.sendall(pickle.dumps(active['Turn']))
            print('Sending Turn({}) [{}]'.format(
                turn, sys.getsizeof(active['Turn'])))
            Game.players[player]['Turn'] = active['Turn']

            update = Game.history[-1]
            conn.sendall(pickle.dumps(update))
            print('Sending Game Update [{}]'.format(
                sys.getsizeof(update)))

            rankings = Game.rankings
            conn.sendall(pickle.dumps(rankings))
            print('Sending Game Rankings [{}]'.format(
                sys.getsizeof(rankings)))

            if Game.players[player]['Turn']:
                played_cards = pickle.loads(conn.recv(2048))
                print('Reciving Cards [{}]'.format(
                    sys.getsizeof(played_cards)))
                value, title = self.get_card(played_cards[0])
                event = f'{player}: {len(played_cards)} {title}({value})'
                self.history.append(event)
                self.network.turn['Value'] = value
                self.network.turn['Quantity'] = len(played_cards)

    def get_card(self, sample_card):
        for rank in self.ranks:
            if sample_card in self.ranks[rank]:
                break
        value = self.ranks.index(rank)
        title = rank
        return value, title

def main():
    game = Screens()
    game.home_screen()

if __name__ == '__main__':
    main()
