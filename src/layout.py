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
        time.sleep(10)

    def dump_English(self):
        for line in English['lower']:
            print(line)

    def pick_random(self, keyboard):
        flat_list = [item for sublist in keyboard for item in sublist]
        return random.choice(flat_list)

    def display_keys(self):
        self.dump_English()

    def __del__(self):
        curses.endwin()


def main():
    keys = Layout()
    signal.signal(signal.SIGINT, keys.__del__)
    print(keys.pick_random(English['lower']))


if __name__ == "__main__":
    main()
