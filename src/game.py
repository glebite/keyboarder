"""
game.py - the exposed game system.
"""
from ast import literal_eval
import configparser
from keyplayer import KeyPlayer
import sys
import time


class Label:
    """Label - helper class for on-screen labels"""
    def __init__(self, description, row, column):
        """__init__ - description, row, column for a Label """
        self.description = description
        self.row = row
        self.column = column

    def info(self):
        return (self.row, self.column, self.description)


class Game:
    """Game - class definition for the game itself
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
        self.goal_label = Label('Current Character:', 4, 55)
        self.score_label = Label('Score:', 7, 55)
        self.pass_label = Label('Pass:', 8, 55)
        self.fail_label = Label('Fail:', 9, 55)
        self.failed_characters = list()
        self.success = 0
        self.fail = 0
        self.first_time = 0
        self.last_time = 0
        self.timed_records = dict()

    def load_game(self):
        """load_game - method for loading the game config file
        """
        self.cfg_parser = configparser.\
            ConfigParser(converters={"any": lambda x: literal_eval(x)})
        try:
            self.cfg_parser.read_file(open(self.game_file, 'r'))
        except FileNotFoundError:
            print(f'Sorry - file not found... {self.game_file}')
            raise FileNotFoundError
            # TODO: something better than Exception - what do we hit?
        except Exception as e:
            print(f'Unexpected exception raised: {e}')
            raise e
        try:
            self._configure_game()
            # TODO: something better than Exception - which one?
        except Exception as e:
            print(e)

    def _configure_game(self):
        """_configure_game - assign tables/variables

        Note: int values get converted from strings
              booleans get converted from strings
        """
        for entry in self.cfg_parser['Game']:
            if self.cfg_parser['Game'][entry].isdigit():
                self.data[entry] =\
                    int(self.cfg_parser['Game'][entry])
            elif self.cfg_parser['Game'][entry] in ['True', 'False']:
                self.data[entry] =\
                    bool(self.cfg_parser['Game'][entry] == 'True')
            else:
                self.data[entry] =\
                    self.cfg_parser['Game'][entry]

    def setup_display(self):
        """setup_display - configuration of the screen

        Note: generally, the labels are straight forward except
              for the case when testing 'words'
        """
        self.player.host_layout.screen_init()
        self.player.host_layout.show_keyboard(0, 0)
        if self.data['words']:
            self.goal_label = Label(4, 55, 'Current word:')
        for label in [self.goal_label,
                      self.score_label,
                      self.pass_label,
                      self.fail_label]:
            self.write_label(label)
        self.player.host_layout.screen.refresh()

    def write_label(self, label):
        self.player.host_layout.screen.addstr(label.row,
                                              label.column,
                                              label.description)

    def hint_on(self, host_char):
        """hint_on - highlights a key on the screen """
        if self.data['hints']:
            self.player.host_layout.key_visibility(host_char, state='ON')
            self.player.host_layout.screen.refresh()

    def hint_off(self, host_char):
        """hint_off - DEhighlights a key on the screen """
        if self.data['hints']:
            self.player.host_layout.key_visibility(host_char, state='OFF')
            self.player.host_layout.screen.refresh()

    def accept_input(self):
        """accept_input - handles user input for the game
        """
        user_input = ''
        key_input = ''
        if self.data['characters']:
            user_input = chr(self.player.host_layout.screen.getch())
        elif self.data['words']:
            while key_input != '\n':
                key_input = chr(self.player.host_layout.screen.getch())
                user_input += key_input
        else:
            # probably change this to a custom Exception and raise it
            print('Unknown state - choose either characters or words')
        return user_input.rstrip()

    def start_clock(self):
        if self.data['timed']:
            self.first_time = time.time()

    def stop_clock(self):
        if self.data['timed']:
            self.last_time = time.time()

    def update_time(self, target):
        if self.data['timed']:
            delta = self.last_time - self.first_time
            self.timed_records[target] = delta

    def update_score(self, in_key, host_char, target_char):
        """update_score - update the display of the score on the screen

        Params:
        in_key      (char) - the incoming key pressed
        host_char   (char) - the key that corresponds to the hardware
        target_char (char) - the learning key that we were hoping for

        Returns:
        n/a

        Raises:
        n/a
        """
        if in_key == host_char:
            self.success += 1
        else:
            self.failed_characters.append(target_char)
            self.fail += 1
        self.player.host_layout.screen.addstr(8, 65, f'{self.success}')
        self.player.host_layout.screen.addstr(9, 65, f'{self.fail}')

    def print_results(self):
        """print_results - final screen output of the user's score
        """
        print(f'Pass: {self.success}')
        print(f'Fail: {self.fail}')
        if self.fail:
            for failed in self.failed_characters:
                print(f'Missed: {failed}')
        for key in self.timed_records:
            print(key, self.timed_records[key])

    def run(self):
        """run - the core of the core of the game:

        Notes:
            1) setup the keyboards
            2) configure the display
            3) loop through a range of characters (or words (TBD)) and:
                a) pick a character (word)
                b) display the desired character
                c) display hinting or not
                d) accept input from the user
                e) turn hinting off
                f) evaluate and update the current score 
            4) close down the display
            5) print the final results
        """
        self.player = KeyPlayer(self.data['host_kbd'], self.data['target_kbd'])
        self.setup_display()

        for game_round in range(self.data['number']):
            target_character = self.player.target.pick_random_key()
            row, column = self.player.target_layout.\
                keyboard.get_key_position(target_character)
            host_char = self.player.host_layout.keyboard.\
                get_char_from_position(row, column)[0]

            self.start_clock()
            self.player.host_layout.screen.addstr(5, 60, target_character)
            self.player.host_layout.screen.refresh()

            self.hint_on(host_char)
            in_key = self.accept_input()
            self.stop_clock()
            self.hint_off(host_char)
            self.update_time(target_character)
            self.update_score(in_key, host_char, target_character)

        self.player.host_layout.screen_deinit()
        self.print_results()


def main(game_file):
    g = Game(game_file)
    print("loading...")
    g.load_game()
    print("Loaded...")
    g.run()


if __name__ == "__main__":
    main(sys.argv[1])
