from keyplayer import KeyPlayer

FARSI = 'src/Farsi_RTL.csv'
ENGLISH = 'src/English.csv'


def test_keyplayer_creation():
    kp = KeyPlayer(FARSI, ENGLISH)
    assert kp, 'Could not create a KeyPlayer object'
