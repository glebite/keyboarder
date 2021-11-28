# from layout2 import Layout
# import layout2
from layout2 import Layout, UPPER_LEFT_CORNER, UPPER_RIGHT_CORNER,\
    HORIZONTAL_BAR, VERTICAL_BAR, LOWER_LEFT_CORNER, LOWER_RIGHT_CORNER,\
    RTL, RTLPOP


def test_layout_creation():
    board = Layout('src/English.csv')
    assert board


def test_layout_creation_missing_file():
    try:
        board = Layout('src/Klingon.csv')
        assert not board
    except FileNotFoundError:
        assert True
    else:
        assert False


def test_layout_dump():
    board = Layout('src/English.csv')
    assert 'a' in board.dump_keyboard()


def test_position_calc_known():
    board = Layout('src/English.csv')
    row, col = board.calculate_position('1')
    assert row == 1 and col == 4, f'row {row} != {1} and col {col} != {4}'


def test_position_calc_unknown():
    board = Layout('src/English.csv')
    row, col = board.calculate_position('ب')
    assert row == -1 and col == -1, f'row {row} != {-1} and col {col} != {-1}'


def test_boxit():
    board = Layout('src/English.csv')
    result = board.boxit('a')
    constructed = UPPER_LEFT_CORNER + HORIZONTAL_BAR +\
        UPPER_RIGHT_CORNER + '\n' +\
        VERTICAL_BAR + 'a' + VERTICAL_BAR + '\n' +\
        LOWER_LEFT_CORNER + HORIZONTAL_BAR + LOWER_RIGHT_CORNER + '\n'
    assert result == constructed


def test_boxit_RTL():
    board = Layout('src/Farsi_RTL.csv')
    result = board.boxit('ا')
    constructed = UPPER_LEFT_CORNER + HORIZONTAL_BAR +\
        UPPER_RIGHT_CORNER + '\n' +\
        VERTICAL_BAR + f'{RTL}ا{RTLPOP}' + VERTICAL_BAR + '\n' +\
        LOWER_LEFT_CORNER + HORIZONTAL_BAR + LOWER_RIGHT_CORNER + '\n'
    assert result == constructed


