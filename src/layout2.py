import kboard
import curses
import time
"""
┏━┓┏━┓┏━┓┏━┓┏━┓┏━┓┏━┓┏━┓┏━┓┏━┓┏━┓┏━┓┏━┓
┃` ┃┃1 ┃┃2 ┃┃3   ┃┃4   ┃┃5  ┃┃6    ┃┃7  ┃┃8   ┃┃9   ┃┃-   ┃┃=   ┃
┗━┛┗━┛┗━┛┗━┛┗━┛┗━┛┗━┛┗━┛┗━┛┗━┛┗━┛┗━┛┗━┛
┏━━━┓┏━┓┏━┓┏━┓┏━┓┏━┓┏━┓┏━┓┏━┓┏━┓┏━┓┏━┓┏━┓┏━┓
┃TAB       ┃┃q  ┃┃w  ┃┃e   ┃┃r   ┃┃t   ┃┃y   ┃┃u  ┃┃i    ┃┃o   ┃┃p  ┃┃[    ┃┃]   ┃┃\   ┃
┗━━━┛┗━┛┗━┛┗━┛┗━┛┗━┛┗━┛┗━┛┗━┛┗━┛┗━┛┗━┛┗━┛┗━┛
┏━━━━┓┏━┓┏━┓┏━┓┏━┓┏━┓┏━┓┏━┓┏━┓┏━┓┏━┓┏━┓
┃CAPS          ┃┃a   ┃┃s  ┃┃d   ┃┃f   ┃┃g   ┃┃h   ┃┃j   ┃┃k   ┃┃l    ┃┃;   ┃┃'    ┃
┗━━━━┛┗━┛┗━┛┗━┛┗━┛┗━┛┗━┛┗━┛┗━┛┗━┛┗━┛┗━┛
┏━━━━━┓┏━┓┏━┓┏━┓┏━┓┏━┓┏━┓┏━┓┏━┓┏━┓┏━┓
┃SHIFT            ┃┃z   ┃┃x   ┃┃c   ┃┃v   ┃┃b  ┃┃n   ┃┃m ┃┃,   ┃┃.     ┃┃/   ┃
┗━━━━━┛┗━┛┗━┛┗━┛┗━┛┗━┛┗━┛┗━┛┗━┛┗━┛┗━┛

Assuming placement of (plc_row=0, plc_column=0)
Wishing to highlight 'w', we would have to:
1) find the key_row, (implied) column  in the keyboard object where Key.lower is 'w'
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

    def calculate_position(self):
        key_row, key_column = self.keyboard.get_key_position('b')
        plc_row = 0
        row = (key_row*3) + 1 + plc_row
        pos = 1
        for item in self.keyboard.layout[key_row]:
            if item.lower == 'b':
                break
            pos += len(item.lower) + 2
        return (row, pos)

def main():
    x = Layout('English.csv')
    row,col = x.calculate_position()
    x.screen_init()
    x.show_keyboard(0, 0)
    x.screen.addstr(row, col, 'b', curses.A_REVERSE)
    x.screen.refresh()
    time.sleep(5)
    # z = x.output_snapshot()
    # print(z)


if __name__ == "__main__":
    main()
