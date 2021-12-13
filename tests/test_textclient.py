from textclient import TextClient
import pytest


def test_textclient_creation():
    tc = TextClient('localhost:5000')
    assert tc, "TextClient not created as expected"


def test_textclient_creation_bad_param():
    with pytest.raises(ValueError):
        tc = TextClient('')
        assert True
    assert False
