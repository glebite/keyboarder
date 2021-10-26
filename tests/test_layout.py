from layout2 import Layout


def test_layout_creation():
    board = Layout('src/English.csv')
    assert board


def test_layout_dump():
    board = Layout('src/English.csv')
    assert 'a' in board.dump_keyboard() 

