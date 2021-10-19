"""keyplayer.py - experimenting game stuff...
"""
import keyboard
import curses



class KeyPlayer(object):
    def __init__(self, target_kbd, host_kbd):
        self.target = keyboard.keyboard(target_kbd)
        self.host = keyboard.keyboard(host_kbd)

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
            lower, upper = self.target.get_char_from_position(row, column)
            try:
                stdscr.addch(lower)
            except Exception as e:
                # yeah - raw exception for now.
                pass

        curses.endwin()


def main(lang1, lang2):
    """
    """
    x = KeyPlayer(lang1, lang2)
    x.sample_test()


if __name__ == "__main__":
    main('Farsi.csv', 'English.csv')
