import kboard
import curses


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


class Layout(object):
    def __init__(self, keyboard_file):
        self.keyboard_file = keyboard_file
        self.keyboard = kboard.Keyboard(self.keyboard_file)
        self.keyboard.read_config()

    def dump_keyboard(self):
        keys = ""
        for row in self.keyboard.layout:
            for key in row:
                keys += f'{key.lower} '
        return keys


def main():
    x = Layout('English.csv')
    x.dump_keyboard()


if __name__ == "__main__":
    main()
