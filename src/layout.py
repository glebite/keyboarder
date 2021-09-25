"""
layout.py
"""
import curses


class Layout(object):
    """
    """
    def __init__(self):
        self.keys = curses.initscr()
        curses.noecho()
        curses.cbreak()

    def __del__(self):
        curses.endwin()


def main():
    pass


if __name__ == "__main__":
    main()
