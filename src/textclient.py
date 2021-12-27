import requests
import sys


class TextClient:
    """TextClient
    """
    def __init__(self, server_ip):
        if ':' not in server_ip:
            raise ValueError
        if 'http://' not in server_ip:
            self.server_ip = 'http://' + server_ip
        else:
            self.server_ip = server_ip
        self.player = None

    def get_key_data(self):
        """get_key_data - retrieve a key from the server
        """
        r = requests.get(self.server_ip + '/pick_key')
        print(r.status_code)

    def get_games_from_server(self):
        """get_games_from_server(self):
        """
        r = requests.get(self.server_ip + '/listgames')
        print(r.status_code)

    def send_game_selection_to_server(self, game):
        """send_game_selection_to_server
        """
        game_data = {'game_choice', game}
        r = requests.post(self.server_ip + '/game_choice', data=game_data)
        print(r.status_code)


if __name__ == "__main__":
    tc = TextClient(sys.argv[1])
    tc.get_key_data()
