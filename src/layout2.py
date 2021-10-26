import kboard
import curses


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
