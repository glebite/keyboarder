import kboard
import curses


class Layout(object):
    def __init__(self, keyboard_file):
        self.keyboard_file = keyboard_file
        self.keyboard = kboard.Keyboard(self.keyboard_file)
        self.keyboard.read_config()

    def dump_keyboard(self):
        for row in self.keyboard.layout:
            for key in row:
                print(f'{key.lower} ', end='')
            print('')


def main():
    x = Layout('English.csv')
    x.dump_keyboard()


if __name__ == "__main__":
    main()
