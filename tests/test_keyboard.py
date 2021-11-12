from kboard import Keyboard


def test_keyboard_creation():
    board = Keyboard('file')
    assert board


def test_read_config():
    board = Keyboard('src/Farsi_RTL.csv')
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
    assert board.get_char_from_position(0, 1) == ['1', '!']


def test_csv_not_found():
    board = Keyboard('src/Russian.csv')
    try:
        board.read_config()
        assert False
    except Exception as e:
        print(f'Examine this to be true: {e}')
        assert True


def test_mapping():
    english = Keyboard('src/English.csv')
    english.read_config()
    farsi = Keyboard('src/Farsi_RTL.csv')
    farsi.read_config()
    row, column = english.get_key_position('k')
    lower, upper = farsi.get_char_from_position(row, column)
    print(lower)
    print(upper)
    assert lower == 'ن'
