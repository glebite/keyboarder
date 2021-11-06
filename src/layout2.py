import kboard
import curses
import time
"""

Assuming placement of (plc_row=0, plc_column=0)
Wishing to highlight 'w', we would have to:
1) find the key_row, (implied) column  in the keyboard object where Key.lower
   is 'w'
2) row = (key_row*3) + 1 + plc_row
3) column = sum of sizes of boxes on a row:
     (TAB + 2) + 1 + 1 ...
"""

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
        curses.curs_set(0)

    def __del__(self):
        curses.curs_set(1)
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
            pos += len(char.lower) + 2

        row += 3
        pos = column
        for char in self.keyboard.layout[1]:
            box = self.boxit(char.lower)
            self.placeit(pos, row, box)
            pos += len(char.lower) + 2

        row += 3
        pos = column

        for char in self.keyboard.layout[2]:
            box = self.boxit(char.lower)
            self.placeit(pos, row, box)
            pos += len(char.lower) + 2

        row += 3
        pos = column
        for char in self.keyboard.layout[3]:
            box = self.boxit(char.lower)
            self.placeit(pos, row, box)
            pos += len(char.lower) + 2

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

    def calculate_position(self, character):
        key_row, key_column = self.keyboard.get_key_position(character)
        plc_row = 0
        row = (key_row*3) + 1 + plc_row
        pos = 1
        for item in self.keyboard.layout[key_row]:
            if item.lower == character:
                break
            pos += len(item.lower) + 2
        return (row, pos)

    def key_visibility(self, character, state='ON'):
        row, column = self.calculate_position(character)
        if state == 'ON':
            self.screen.addstr(row, column, character, curses.A_STANDOUT)
        else:
            self.screen.addstr(row, column, character, curses.A_NORMAL)
        self.screen.refresh()


def main():
    try:
        x = Layout('English.csv')
        y = Layout('Farsi_RTL.csv')
        r = y.keyboard.layout[2][4].lower
        (row, col) = y.keyboard.get_key_position(r)
        char = x.keyboard.get_char_from_position(row, col)[0]
        x.screen_init()
        x.show_keyboard(0, 0)
        x.screen.refresh()
        x.key_visibility(char, state='ON')
        time.sleep(5)
        x.key_visibility(char, state='OFF')
        time.sleep(5)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
