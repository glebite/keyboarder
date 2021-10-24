from layout2 import Layout


def test_layout_creation():
    board = Layout('src/English.csv')
    assert board
