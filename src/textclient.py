import requests
import sys
import json
from layout2 import Layout
import time
import text_menu
import curses


class TextClient:
    """TextClient
    """
    def __init__(self, server_ip):
        """__init__ - init of the class

        Should converts the incoming server_ip from
        address:port to http://address:port if need be.

        params:
        server_ip - the location of the gameengine server

        returns:
        n/a

        raises:
        n/a
        """
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
        return r

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
        return r

    def temp_user_game_selection(self):
        """temp_user_game_selection - temporary until display mechanism is
        put together.
        """
        available_games = self.get_games_from_server()
        screen = curses.initscr()
        curses.curs_set(0)
        main_menu_items = list()

        for i, game in enumerate(available_games['game_list']):
            main_menu_items.append((game, i))

        main_menu = text_menu.Menu(main_menu_items, screen)

        main_menu.display()
        curses.curs_set(1)
        curses.endwin()
        self.selection = main_menu.selection
        return main_menu.selection

    def temp_user_pick_game(self):
        """temp_user_pick_game - temporary until display mechanism is
        put together.
        """
        rc = self.send_game_selection_to_server(self.selection)
        return rc

    def temp_get_game_information(self):
        r = requests.get(self.server_ip + '/get_game_status')
        return json.loads(r.text)

    def temp_get_game_data(self):
        r = requests.get(self.server_ip + '/get_game_data')
        return json.loads(r.text)

    def send_key(self, value):
        r = requests.post(self.server_ip + '/receive_key',
                          json={"host_key": value})
        return r.text


if __name__ == "__main__":  # pragma: nocover
    tc = TextClient(sys.argv[1])
    tc.temp_user_game_selection()
    tc.temp_user_pick_game()

    game_information = tc.temp_get_game_information()
    game_counter = game_information['game_status']['remaining']

    stuff = tc.temp_get_game_data()
    layout = Layout(stuff['host_kbd'])
    layout.screen_init()
    layout.show_keyboard()
    layout.screen.refresh()
    layout.placeit(50, 5,  'match the key for')
    layout.screen.refresh()

    while game_counter > 0:
        r = tc.get_key_data()
        target_char = json.loads(r.text)['target']
        layout.placeit(50, 5, f'match the key for {target_char}')
        host_key = layout.screen.getch()
        x = tc.send_key(host_key)
        game_information = tc.temp_get_game_information()
        game_counter = game_information['game_status']['remaining']
        layout.screen.refresh()
        layout.placeit(50, 6, f'remaining guesses: {game_counter:4}')
        success = game_information['game_status']['scores']['success']
        fail = game_information['game_status']['scores']['fail']
        layout.placeit(50, 7, f'scores: {success:4} vs {fail:4}')

    layout.screen_deinit()

    game_information = tc.temp_get_game_information()
    success = game_information['game_status']['scores']['success']
    fail = game_information['game_status']['scores']['fail']
    print(f'scores: {success:4} vs {fail:4}')
