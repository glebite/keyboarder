from key import Key


def test_key_creation():
    key = Key(1,1,1,'x','X')
    if not key:
        assert False
