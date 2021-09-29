"""
layout.py
"""
import curses
import signal
import time
from array import *

English = dict()
English['lower'] = {'` 1 2 3 4 5 6 7 8 9 0 - = ',
                    'q w e r t y u i o p [ ] \' ',
                    'a s d f g h j k  l ; \\ ',
                    'z x c v b n m , . / '}
English['upper'] = {'~ ! @ # $ % ^ & * ( ) _ + ',
                    'Q W E R T Y U I O P { } | ',
                    'A S D F G H J K L : \"',
                    'Z X C V B N M < > ? '}

Farsi = ['‍', '۱', '۲', '۳', '۴', '۵','۶', '۷', '۸', '۹', '۰', '-' , '=']


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
