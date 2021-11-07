"""keyplayer.py - experimenting game stuff...
"""
import kboard
import layout2
import time
import curses


class KeyPlayer(object):
    def __init__(self, host_kbd, target_kbd):
        self.target = kboard.Keyboard(target_kbd)
        self.host = kboard.Keyboard(host_kbd)
        self.target.read_config()
        self.host.read_config()
        self.target_layout = layout2.Layout(target_kbd)
        self.host_layout = layout2.Layout(host_kbd)
        self.key_correct = 0
        self.key_presses = 0

    def clear_score(self):
        self.key_presses = 0
        self.key_correct = 0


def main(lang1, lang2):
    """
    """
    player = KeyPlayer(lang1, lang2)
    player.host_layout.screen_init()
    player.host_layout.show_keyboard(0, 0)
    player.host_layout.screen.refresh()
    # player.host_layout.demo_cool(player.target_layout)
    target_character = 'ت'
    row, column = player.target_layout.\
        keyboard.get_key_position(target_character)
    host_char = player.host_layout.keyboard.\
        get_char_from_position(row, column)[0]
    player.host_layout.key_visibility(host_char, state='ON')
    player.host_layout.screen.addstr(5, 60, target_character)
    player.host_layout.screen.refresh()
    in_key = None

    # import pdb; pdb.set_trace()
    while in_key != '`':
        in_key = chr(player.host_layout.screen.getch())
        if in_key == host_char:
            print(f'Yay! {in_key} matches!')
        else:
            print(f'Boo - {in_key} does not match {host_char}')
        time.sleep(1)


if __name__ == "__main__":
    main('English.csv', 'Farsi_RTL.csv')
