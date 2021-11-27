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
