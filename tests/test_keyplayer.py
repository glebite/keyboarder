from keyplayer import KeyPlayer

FARSI = 'src/Farsi_RTL.csv'
ENGLISH = 'src/English.csv'


def test_keyplayer_creation():
    kp = KeyPlayer(FARSI, ENGLISH)
    assert kp, 'Could not create a KeyPlayer object'


def test_keyplayer_pick_random():
    kp = KeyPlayer(FARSI, ENGLISH)
    target, host = kp.from_target_pick_host()
    assert target, f'Target not created: {target}'
    assert host, f'Host not created: {host}'
