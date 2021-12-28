import requests
import sys
import json


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
        return r.status_code

    def get_games_from_server(self):
        """get_games_from_server(self):
        """
        r = requests.get(self.server_ip + '/list_games')
        return json.loads(r.text)

    def send_game_selection_to_server(self, game):
        """send_game_selection_to_server

        params:
        game - string - the game to be selected

        returns:
        n/a

        raises:
        n/a
        """
        r = requests.post(self.server_ip + '/game_choice',
                          json={"game_choice": game})
        return r.status_code

    def temp_user_game_selection(self):
        available_games = self.get_games_from_server()
        print(available_games)
        for i, game in enumerate(available_games['game_list']):
            print(i, game)

    def temp_user_pick_game(self):
        print('Enter your choice: ')
        choice = input()
        rc = self.send_game_selection_to_server(choice)
        if rc.status_code == 200:
            print("Okidoki")
        else:
            print("Nokidoki")


if __name__ == "__main__":  # pragma: nocover
    tc = TextClient(sys.argv[1])
    tc.temp_user_game_selection()
    tc.temp_user_pick_game()
