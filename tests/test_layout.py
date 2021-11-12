from layout2 import Layout


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
