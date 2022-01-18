"""
Heavily lifted and modified from:
https://stackoverflow.com/questions/14200721/how-to-create-a-menu-and-submenus-in-python-curses
"""
import curses
from curses import panel
import time


class Menu(object):
    """
    """
    def __init__(self, items, stdscreen):
        """
        """
        self.window = stdscreen.subwin(0, 0)
        self.window.keypad(1)
        self.panel = panel.new_panel(self.window)
        self.panel.hide()
        curses.doupdate()
        self.selection = None
        panel.update_panels()

        self.position = 0
        self.items = items
        self.items.append(("exit", "exit"))
        time.sleep(10)

    def navigate(self, n):
        """
        """
        self.position += n
        if self.position < 0:
            self.position = 0
        elif self.position >= len(self.items):
            self.position = len(self.items) - 1

    def display(self):
        """
        """
        self.panel.top()
        self.panel.show()
        self.window.clear()

        while True:
            self.window.refresh()
            curses.doupdate()
            for index, item in enumerate(self.items):
                if index == self.position:
                    mode = curses.A_REVERSE
                else:
                    mode = curses.A_NORMAL

                msg = "%s" % (item[0])
                self.window.addstr(1 + index, 1, msg, mode)

            key = self.window.getch()

            if key in [curses.KEY_ENTER, ord("\n")]:
                if self.position == len(self.items) - 1:
                    break
                else:
                    self.selection = self.items[self.position][0]
                    print(f'Choosing: {self.selection}')
                    break

            elif key == curses.KEY_UP:
                self.navigate(-1)

            elif key == curses.KEY_DOWN:
                self.navigate(1)

        self.window.clear()
        self.panel.hide()
        panel.update_panels()
        curses.doupdate()


class MyApp(object):
    def __init__(self, stdscreen):
        self.screen = stdscreen
        curses.curs_set(0)

        main_menu_items = [
            ("game_1.py", curses.beep),
            ("game_2.py", curses.flash),
        ]
        self.main_menu = Menu(main_menu_items, self.screen)
        # self.main_menu.display()
        curses.curs_set(1)
        curses.endwin()


if __name__ == "__main__":
    m = MyApp(curses.initscr())
    print(m.main_menu.selection)
