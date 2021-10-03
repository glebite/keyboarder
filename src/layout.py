"""
layout.py
"""
import curses
import signal
import random
import time

UPPER_LEFT_CORNER = u'\u250f'
UPPER_RIGHT_CORNER = u'\u2513'
LOWER_LEFT_CORNER = u'\u2517'
LOWER_RIGHT_CORNER = u'\u251b'
HORIZONTAL_BAR = u'\u2501'
VERTICAL_BAR = u'\u2503'
CROSS_BAR = u'\u254b'
LEFT_VERTICAL_T = u'\u2523'
RIGHT_VERTICAL_T = u'\u252b'
HORIZONTAL_DOWN_T = u'\u2533'
HORIZONTAL_UP_T = u'\u253b'

English = dict()
English['lower'] = ['`1234567890-=',
                    'qwertyuiop[]\\',
                    'asdfghjkl;\'',
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
        pass

    def pick_random(self, keyboard):
        flat_list = [item for sublist in keyboard for item in sublist]
        return random.choice(flat_list)

    def find_keyat(self, keyboard, char):
        for i, row in enumerate(keyboard):
            if char in row:
                return (i, row.find(char))
        return (-1, -1)

    def boxit(self, contents):
        """
        """
        box = UPPER_LEFT_CORNER
        for i in contents:
            box += HORIZONTAL_BAR
        box += UPPER_RIGHT_CORNER
        box += "\n"
        box += VERTICAL_BAR
        box += contents
        box += VERTICAL_BAR
        box += "\n"
        box += LOWER_LEFT_CORNER
        for i in contents:
            box += HORIZONTAL_BAR
        box += LOWER_RIGHT_CORNER
        box += "\n"
        return box

    def placeit(self, x, y, it):
        row = y
        col = x
        for i, character in enumerate(it):
            self.screen.addstr(row, col, character)
            if character == "\n":
                row += 1
                col = x
            else:
                col += 1

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
    box = keys.boxit('SHIFT')
    keys.placeit(1, 4, box)
    pos = 8
    for char in English['lower'][3]:
        box = keys.boxit(char)
        keys.placeit(pos, 4, box)
        pos += 3

    keys.screen.refresh()
    time.sleep(10)
    # x = keys.process_key()
    # del keys


if __name__ == "__main__":
    print(main())
