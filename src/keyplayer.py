"""keyplayer.py - experimenting game stuff...
"""
import kboard
import layout2


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
    success = 0
    fail = 0
    player = KeyPlayer(lang1, lang2)
    player.host_layout.screen_init()
    player.host_layout.show_keyboard(0, 0)
    player.host_layout.screen.refresh()

    for game_round in range(10):
        # target_character = player.target.pick_random_key()
        # import pdb
        # pdb.set_trace()
        # target_character = player.target.keyboard.pick_random_key()
        target_character = player.target_layout.\
            keyboard.layout[3][game_round].lower
        if len(target_character) > 3:
            continue
        row, column = player.target_layout.\
            keyboard.get_key_position(target_character)
        host_char = player.host_layout.keyboard.\
            get_char_from_position(row, column)[0]
        player.host_layout.key_visibility(host_char, state='ON')
        player.host_layout.screen.addstr(5, 60, target_character)
        player.host_layout.screen.refresh()

        in_key = chr(player.host_layout.screen.getch())
        player.host_layout.key_visibility(host_char, state='OFF')

        if in_key == host_char:
            success += 1
        else:
            fail += 1
    player.host_layout.screen_deinit()
    print(success, fail)


if __name__ == "__main__":
    main('English.csv', 'Farsi_RTL.csv')
