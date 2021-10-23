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
