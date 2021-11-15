import configparser


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
        self.cfg_parser = configparser.ConfigParser()
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


def main():
    g = Game('../data/game_1.cfg')
    g.load_game()


if __name__ == "__main__": main()
