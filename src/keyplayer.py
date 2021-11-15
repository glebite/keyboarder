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


def main(lang1, lang2):   # pragma: nocover
    """
    """
    keys_to_ignore = ['TAB', 'CAPS', 'SHIFT']
    success = 0
    fail = 0
    failed_characters = list()
    player = KeyPlayer(lang1, lang2)
    player.host_layout.screen_init()
    player.host_layout.show_keyboard(0, 0)
    player.host_layout.screen.refresh()

    player.host_layout.screen.addstr(4, 55, 'Current Character:')
    player.host_layout.screen.addstr(7, 55, 'Score: ')
    player.host_layout.screen.addstr(8, 55, 'Success: ')
    player.host_layout.screen.addstr(9, 55, 'Fail:    ')

    for game_round in range(self.data['number']):
        target_character = player.target.pick_random_key()

        if len(target_character) > 3 or target_character in keys_to_ignore:
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
            failed_characters.append(target_character)
            fail += 1
        player.host_layout.screen.addstr(8, 65, f'{success}')
        player.host_layout.screen.addstr(9, 65, f'{fail}')

    player.host_layout.screen_deinit()
    print(f'Pass: {success}')
    print(f'Fail: {fail}')
    if fail:
        for failed in failed_characters:
            print(f'Missed: {failed}')


if __name__ == "__main__":
    main('English.csv', 'Farsi_RTL.csv')  # pragma: nocover
