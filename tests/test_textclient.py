from textclient import TextClient


def test_textclient_creation():
    tc = TextClient('localhost:5000')
    assert tc, "TextClient not created as expected"


def test_textclient_creation_bad_param():
    try:
        tc = TextClient('slocalhost')
        print(tc)
        assert False
    except ValueError:
        assert True
