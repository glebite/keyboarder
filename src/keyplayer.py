import keyboard
import curses


def main(lang1, lang2):
    """
    """
    target = keyboard.keyboard(lang1)
    host = keyboard.keyboard(lang2)
    host.read_config()
    target.read_config()
    stdscr = curses.initscr()
    curses.cbreak()
    stdscr.keypad(1)

    key = ''
    while key != ord('q'):
        key = stdscr.getch()
        row, column = host.get_key_position(chr(key))
        lower, upper = target.get_char_from_position(row, column)
        stdscr.addch(upper)


if __name__ == "__main__":
    main('Farsi.csv', 'English.csv')
