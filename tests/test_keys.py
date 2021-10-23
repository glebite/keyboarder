from key import Key


def test_key_creation():
    piece = Key(1, 1, 1, 'x', 'X')
    if not piece:
        assert False


def test_key_rowcolumn():
    piece = Key(1, 2, 1, 'x', 'X')
    assert piece.row == 1
    assert piece.column == 2


def test_key_upperlower():
    piece = Key(1, 2, 1, 'x', 'X')
    assert piece.lower == 'x'
    assert piece.upper == 'X'


def test_str_output():
    piece = Key(1, 3, 1, 'y', 'Y')
    assert piece.__str__() == "1 3 1 y Y"


def test_isvisible():
    piece = Key(1, 3, 1, 'y', 'Y')
    assert piece.is_visible()


def test_is_not_visible():
    piece = Key(1, 3, 0, 'y', 'Y')
    assert not piece.is_visible()


def test_range_row_low():
    try:
        piece = Key(-1, 3, 1, 'z', 'Z')
        piece.is_visible()
        assert False
    except Exception:
        assert True


def test_range_row_high():
    try:
        piece = Key(26, 3, 1, 'z', 'Z')
        piece.is_visible()
        assert False
    except Exception:
        assert True


def test_range_col_low():
    try:
        piece = Key(5, -2, 1, 'z', 'Z')
        piece.is_visible()
        assert False
    except Exception:
        assert True


def test_range_col_high():
    try:
        piece = Key(5, 85, 1, 'z', 'Z')
        piece.is_visible()
        assert False
    except Exception:
        assert True
