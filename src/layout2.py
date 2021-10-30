import kboard
import curses
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


class Layout():
    def __init__(self, keyboard_file):
        """Layout - layout class - probably a base class eventually
        """
        self.keyboard_file = keyboard_file
        self.keyboard = kboard.Keyboard(self.keyboard_file)
        self.keyboard.read_config()

    def screen_init(self):
        """screen_init - curses initialization method
        """
        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()

    def __del__(self):
        """__del__ - cleanup of curses artifacts, etc...
        """
        curses.endwin()

    def dump_keyboard(self):
        keys = ""
        for row in self.keyboard.layout:
            for key in row:
                keys += f'{key.lower} '
        return keys

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
        for character in it:
            # print(row, col, character)
            self.screen.addstr(row, col, character)
            if character == "\n":
                row += 1
                col = x
            else:
                col += 1

    def show_keyboard(self):
        box = self.boxit('')
        self.placeit(3, 1, box)
        pos = 3
        for char in self.keyboard.layout[0]:
            box = self.boxit(char.lower)
            # print(pos, 1, char)
            self.placeit(pos, 1, box)
            pos += 3

        box = self.boxit('TAB')
        self.placeit(1, 4, box)
        pos = 7
        for char in self.keyboard.layout[1]:
            box = self.boxit(char.lower)
            self.placeit(pos, 4, box)
            pos += 3

        box = self.boxit('LOCK')
        self.placeit(1, 7, box)
        pos = 7
        for char in self.keyboard.layout[2]:
            box = self.boxit(char.lower)
            self.placeit(pos, 7, box)
            pos += 3

        box = self.boxit('SHIFT')
        self.placeit(1, 10, box)
        pos = 8
        for char in self.keyboard.layout[3]:
            box = self.boxit(char.lower)
            self.placeit(pos, 10, box)
            pos += 3


def main():
    x = Layout('English.csv')
    x.screen_init()
    x.show_keyboard()
    x.screen.refresh()

    time.sleep(10)

    print("Done!")


if __name__ == "__main__":
    main()
