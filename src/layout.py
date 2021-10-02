"""
layout.py
"""
import curses
import signal
import time
import random


English = dict()
English['lower'] = ['`1234567890-=',
                    'qwertyuiop[]\'',
                    'asdfghjkl;\\',
                    'zxcvbnm,./']
English['upper'] = ['~!@#$%^&*()_+',
                    'QWERTYUIOP{}|',
                    'ASDFGHJKL:\"',
                    'ZXCVBNM<>?']

Farsi = dict()
Farsi['lower'] = ['‍۱۲۳۴۵۶۷۸۹۰-=',
                  'ضصثقفغعهخحجچ\\',
                  'شسیبلاتنمکگ',
                  'ظطزرذدپو./']
Farsi['upper'] = ['÷!٬٫﷼٪×،*)(ـ+',
                  'ًٌٍَُِّْ][}{|',
                  'ؤئيإأآة»«:؛',
                  'كٓژٰ‌ٔء><؟']


class Layout(object):
    """
    """
    def __init__(self):
        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.screen.clear()

    def pick_random(self, keyboard):
        flat_list = [item for sublist in keyboard for item in sublist]
        return random.choice(flat_list)

    def find_keyat(self, keyboard, char):
        for i, row in enumerate(keyboard):
            if char in row:
                return (i, row.find(char))
        return (-1, -1)

    def boxit(self, keyboard):
        """
        ----------------------------------
        |`|1|2|3|4|5|6|7|8|9|0|-|=|
        ----------------------------------
        13
        13
        11
        10
        """
        for i, row in enumerate(keyboard):
            for char in row:
                print('+-', end='')
            print('+')

    def __del__(self):
        curses.endwin()
        pass

    def process_key(self):
        while True:
            k = self.screen.get_wch()
            matching = self.find_keyat(English['lower'], k)
            print(Farsi['lower'][matching[0]][matching[1]])


def main():
    keys = Layout()
    signal.signal(signal.SIGINT, keys.__del__)
    # matching = keys.find_keyat(English['lower'], '\\')
    # print(Farsi['lower'][matching[0]][matching[1]])
    # keys.boxit(English['lower'])
    x = keys.process_key()
    del keys
    return(x)


if __name__ == "__main__":
    print(main())
