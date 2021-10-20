"""keyplayer.py - experimenting game stuff...
"""
import keyboard
import curses


class KeyPlayer(object):
    def __init__(self, target_kbd, host_kbd):
        self.target = keyboard.keyboard(target_kbd)
        self.host = keyboard.keyboard(host_kbd)
        self.key_correct = 0
        self.key_presses = 0

    def sample_test(self):
        """
        """
        self.host.read_config()
        self.target.read_config()
        stdscr = curses.initscr()
        curses.cbreak()
        stdscr.keypad(1)

        key = ''
        while key != ord('q'):
            key = stdscr.getch()
            row, column = self.host.get_key_position(chr(key))
            print(row, column)
            lower, upper = self.target.get_char_from_position(row, column)
            try:
                stdscr.addch(lower)
                stdscr.addch(upper)
            except Exception as e:
                # yeah - raw exception for now.
                print(e)
        curses.endwin()

    def debugging(self):
        """
        """
        self.host.read_config()
        self.target.read_config()
        for rows in self.host.layout:
            for key in rows:
                row, column = self.host.get_key_position(key.lower)
                print(row, column, key.lower, self.target.get_char_from_position(row, column))


    def clear_score(self):
        self.key_presses = 0
        self.key_correct = 0


def main(lang1, lang2):
    """
    """
    x = KeyPlayer(lang1, lang2)
    x.debugging()


if __name__ == "__main__":
    main('Farsi.csv', 'English.csv')
