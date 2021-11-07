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
    player = KeyPlayer(lang1, lang2)
    # import pdb; pdb.set_trace()
    player.host_layout.screen_init()
    player.host_layout.show_keyboard(0, 0)
    player.host_layout.screen.refresh()
    player.host_layout.demo_cool(player.target_layout)


if __name__ == "__main__":
    main('English.csv', 'Farsi_RTL.csv')
