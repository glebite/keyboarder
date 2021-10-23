from kboard import Keyboard


def test_keyboard_creation():
    board = Keyboard('file')
    assert board


def test_read_config():
    board = Keyboard('src/Farsi.csv')
    board.read_config()
