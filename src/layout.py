"""
layout.py
"""
import curses
import signal
import time


class Layout(object):
    """
    """
    def __init__(self):
        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.screen.clear()
        time.sleep(10)

    def display_keys(self):
        pass

    def __del__(self):
        curses.endwin()


def main():
    keys = Layout()
    signal.signal(signal.SIGINT, keys.__del__)
    keys.display_keys()


if __name__ == "__main__":
    main()
