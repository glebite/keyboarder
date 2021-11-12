from keyplayer import KeyPlayer

FARSI = 'src/Farsi_RTL.csv'
ENGLISH = 'src/English.csv'


def test_keyplayer_creation():
    kp = KeyPlayer(FARSI, ENGLISH)
    assert kp, 'Could not create a KeyPlayer object'


def test_clear_score():
    kp = KeyPlayer(FARSI, ENGLISH)
    kp.key_correct = 1
    kp.key_presses = 3
    assert kp.key_correct == 1 and kp.key_presses == 3, \
        'Failed to set kp attributes'
    kp.clear_score()
    assert kp.key_correct == 0 and kp.key_presses == 0, \
        'Failed to set kp attributes'
