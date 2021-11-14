import configparser


class Game:
    """
    """
    def __init__(self, game_file):
        self.game_file = game_file

    def load_game(self):
        self.cfg_parser = configparser.ConfigParser()
        try:
            self.cfg_parser.read_file(open(self.game_file, 'r'))
        except FileNotFoundError:
            print(f'Sorry - file not found... {self.game_file}')
            raise FileNotFoundError
        except Exception as e:
            print(f'Exception raised: {e}')
        print(self.cfg_parser.sections)
