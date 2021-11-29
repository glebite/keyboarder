# from layout2 import Layout
# import layout2
from layout2 import Layout, UPPER_LEFT_CORNER, UPPER_RIGHT_CORNER,\
    HORIZONTAL_BAR, VERTICAL_BAR, LOWER_LEFT_CORNER, LOWER_RIGHT_CORNER,\
    RTL, RTLPOP
import curses


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


def test_key_position_default():
    board = Layout('src/English.csv')
    board.screen_init()
    board.show_keyboard(0, 0)
    screen = board.screen_dump()
    value = screen['1,4']
    assert value == 49, f'Expected 49, got {value} instead.'
    board.screen_deinit()


def test_key_hint_on():
    board = Layout('src/English.csv')
    board.screen_init()
    board.show_keyboard(0, 0)
    board.key_visibility('1')
    screen = board.screen_dump()
    value = screen['1,4']
    expected = ord('1') | curses.A_STANDOUT
    assert value == expected, f'Expected {expected}, got {value} instead.'
    board.screen_deinit()


def test_key_hint_off():
    board = Layout('src/English.csv')
    board.screen_init()
    board.show_keyboard(0, 0)
    board.key_visibility('1')
    board.key_visibility('1', 'OFF')
    screen = board.screen_dump()
    value = screen['1,4']
    expected = ord('1')
    assert value == expected, f'Expected {expected}, got {value} instead.'
    board.screen_deinit()
