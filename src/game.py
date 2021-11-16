from ast import literal_eval
import configparser
from keyplayer import KeyPlayer
import time


class Label:
    def __init__(self, description, row, column):
        self.description = description
        self.row = row
        self.column = column
    

class Game:
    """
    """
    def __init__(self, game_file):
        self.game_file = game_file
        self.data = {'name': None,
                     'description': None,
                     'characters': None,
                     'timed': None,
                     'hints': None,
                     'number': None,
                     'words': None,
                     'word_file': None,
                     'host_kbd': None,
                     'target_kbd': None}
        self.goal_label = Label('Current Character', 4, 55)
        self.score_label = Label('Score', 7, 55)
        self.pass_label = Label('Pass', 8, 55)
        self.fail_label = Label('Fail', 9, 55)

    def load_game(self):
        self.cfg_parser = configparser.\
            ConfigParser(converters={"any": lambda x: literal_eval(x)})
        try:
            self.cfg_parser.read_file(open(self.game_file, 'r'))
        except FileNotFoundError:
            print(f'Sorry - file not found... {self.game_file}')
            raise FileNotFoundError
        except Exception as e:
            print(f'Unexpected exception raised: {e}')
            raise e
        try:
            self._configure_game()
        except Exception as e:
            print(e)

    def _configure_game(self):
        for entry in self.cfg_parser['Game']:
            if self.cfg_parser['Game'][entry].isdigit():
                self.data[entry] =\
                    int(self.cfg_parser['Game'][entry])
            elif self.cfg_parser['Game'][entry] in ['True', 'False']:
                self.data[entry] =\
                    bool(self.cfg_parser['Game'][entry] is True)
            else:
                self.data[entry] =\
                    self.cfg_parser['Game'][entry]

    def setup_display(self):
        self.player.host_layout.screen_init()
        self.player.host_layout.show_keyboard(0, 0)
        if self.data['words']:
            self.player.host_layout.screen.addstr(4, 55, 'Current Word:')
        else:
            self.player.host_layout.screen.addstr(4, 55, 'Current Character:')
        self.player.host_layout.screen.addstr(7, 55, 'Score: ')
        self.player.host_layout.screen.addstr(8, 55, 'Success: ')
        self.player.host_layout.screen.addstr(9, 55, 'Fail:    ')
        self.player.host_layout.screen.refresh()

    def run(self):
        success = 0
        fail = 0
        failed_characters = list()
        keys_to_ignore = ['TAB', 'CAPS', 'SHIFT']

        self.player = KeyPlayer(self.data['host_kbd'], self.data['target_kbd'])
        self.setup_display()

        for game_round in range(self.data['number']):
            target_character = self.player.target.pick_random_key()

            if len(target_character) > 3 or target_character in keys_to_ignore:
                continue
            row, column = self.player.target_layout.\
                keyboard.get_key_position(target_character)
            host_char = self.player.host_layout.keyboard.\
                get_char_from_position(row, column)[0]
            self.player.host_layout.screen.addstr(5, 60, target_character)
            self.player.host_layout.screen.refresh()

            if self.data['hints']:
                self.player.host_layout.key_visibility(host_char, state='ON')

            in_key = chr(self.player.host_layout.screen.getch())
            if self.data['hints']:
                self.player.host_layout.key_visibility(host_char, state='OFF')

            if in_key == host_char:
                success += 1
            else:
                failed_characters.append(target_character)
                fail += 1
            self.player.host_layout.screen.addstr(8, 65, f'{success}')
            self.player.host_layout.screen.addstr(9, 65, f'{fail}')

        self.player.host_layout.screen_deinit()
        print(f'Pass: {success}')
        print(f'Fail: {fail}')
        if fail:
            for failed in failed_characters:
                print(f'Missed: {failed}')


def main():
    g = Game('../data/game_1.cfg')
    g.load_game()
    g.run()


if __name__ == "__main__":
    main()
