from kboard import Keyboard


def test_keyboard_creation():
    board = Keyboard('file')
    assert board


def test_read_config():
    board = Keyboard('src/Farsi.csv')
    board.read_config()


def test_get_key_position():
    board = Keyboard('src/English.csv')
    board.read_config()
    assert board.get_key_position('1') == (0, 1)


def test_get_bad_key_position():
    board = Keyboard('src/English.csv')
    board.read_config()
    assert board.get_key_position(' ') == (-1, -1)


def test_get_char_from():
    board = Keyboard('src/English.csv')
    board.read_config()
    assert board.get_char_from_position(0, 1) == {'!', '1'}
