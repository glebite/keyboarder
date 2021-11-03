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
RTL = u'\u2067'
RTLPOP = u'\u2069'
LTRDIR = 0
RTLDIR = 1


class Layout():
    def __init__(self, keyboard_file):
        """Layout - layout class - probably a base class eventually
        """
        self.keyboard_file = keyboard_file
        self.keyboard = kboard.Keyboard(self.keyboard_file)
        self.keyboard.read_config()
        if 'RTL' in keyboard_file:
            self.direction = RTLDIR
        else:
            self.direction = LTRDIR

    def screen_init(self):
        """screen_init - curses initialization method
        """
        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()

    def __del__(self):
        curses.endwin()

    def boxit(self, contents):
        """
        """
        box = UPPER_LEFT_CORNER
        for i in contents:
            box += HORIZONTAL_BAR
        box += UPPER_RIGHT_CORNER
        box += "\n"
        box += VERTICAL_BAR
        if self.direction == RTLDIR:
            box += f'{RTL}{contents}{RTLPOP}'
        else:
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
            self.screen.addstr(row, col, character)
            if character == "\n":
                row += 1
                col = x
            else:
                col += 1

    def show_keyboard(self, row=1, column=1):
        pos = column
        for char in self.keyboard.layout[0]:
            box = self.boxit(char.lower)
            self.placeit(pos, row, box)
            pos += 3

        row += 3
        box = self.boxit('TAB')
        self.placeit(column, row, box)
        pos = 6
        for char in self.keyboard.layout[1]:
            box = self.boxit(char.lower)
            self.placeit(pos, row, box)
            pos += 3

        row += 3
        box = self.boxit('CAPS')
        self.placeit(column, row, box)
        pos = 7
        for char in self.keyboard.layout[2]:
            box = self.boxit(char.lower)
            self.placeit(pos, row, box)
            pos += 3

        row += 3
        box = self.boxit('SHIFT')
        self.placeit(column, row, box)
        pos = 8
        for char in self.keyboard.layout[3]:
            box = self.boxit(char.lower)
            self.placeit(pos, row, box)
            pos += 3

    def snapshot(self):
        height, width = self.screen.getmaxyx()
        screen = list()
        row_info = list()
        for row in range(height):
            for col in range(width):
                row_info.append(self.screen.inch(row, col))
            screen.append(row_info)
            row_info = []
        return screen

    def output_snapshot(self):
        snap = self.snapshot()
        lines = ''
        for row in snap:
            for col_char in row:
                if col_char > 255:
                    col_char = 0
                lines += chr(int(col_char))
            lines += '\n\r'
        return lines


def main():
    x = Layout('English.csv')
    x.screen_init()
    x.show_keyboard(1, 1)
    x.screen.refresh()
    time.sleep(1)
    z = x.output_snapshot()
    print(z)


if __name__ == "__main__":
    main()
