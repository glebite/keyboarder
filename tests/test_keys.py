from key import Key


def test_key_creation():
    piece = Key(1,1,1,'x','X')
    if not piece:
        assert False
