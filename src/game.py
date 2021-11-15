from ast import literal_eval
import configparser
from keyplayer import KeyPlayer
import time


class Game:
    """
    """
    def __init__(self, game_file):
        self.game_file = game_file
        self.data = {'name': None,
                     'description': None,
                     'characters': True,
                     'hints': True,
                     'number': 10,
                     'words': False,
                     'timed': False,
                     'word_file': None,
                     'host_kbd': None,
                     'target_kdb': None}

    def load_game(self):
        self.cfg_parser = configparser.ConfigParser(converters={"any": lambda x: literal_eval(x)})
        try:
            self.cfg_parser.read_file(open(self.game_file, 'r'))
        except FileNotFoundError:
            print(f'Sorry - file not found... {self.game_file}')
            raise FileNotFoundError
        except Exception as e:
            print(f'Unexpected exception raised: {e}')
            raise e
        self._configure_game()

    def _configure_game(self):
        for entry in self.cfg_parser['Game']:
            self.data[entry] = self.cfg_parser['Game'][entry]
        print(self.data)

    def run(self):
        player = KeyPlayer(self.data['host_kbd'], self.data['target_kbd'])
        player.host_layout.screen_init()
        player.host_layout.show_keyboard(0, 0)
        if self.data['words']:
            player.host_layout.screen.addstr(4, 55, 'Current Word:')
        else:
            player.host_layout.screen.addstr(4, 55, 'Current Character:')
        player.host_layout.screen.addstr(7, 55, 'Score: ')
        player.host_layout.screen.addstr(8, 55, 'Success: ')
        player.host_layout.screen.addstr(9, 55, 'Fail:    ')
        player.host_layout.screen.refresh()
        time.sleep(10)


def main():
    g = Game('../data/game_1.cfg')
    g.load_game()
    g.run()


if __name__ == "__main__": main()
