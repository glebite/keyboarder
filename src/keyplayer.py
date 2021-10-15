import keyboard
import curses


def main():
    """
    """
    f = keyboard.keyboard('Farsi.csv')
    e = keyboard.keyboard('English.csv')
    e.read_config()
    f.read_config()
    stdscr = curses.initscr()
    curses.cbreak()
    stdscr.keypad(1)

    key = ''
    while key != ord('q'):
        key = stdscr.getch()
        row, column = e.get_key_position(chr(key))
        print(f.get_char_from_position(row, column), end='')


if __name__ == "__main__":
    main()
