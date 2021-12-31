from textclient import TextClient
import pytest
import subprocess
import socket
import time
import requests


def wait_until_up(watchdog):
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('127.0.0.1', 5000))
            s.close()
            break
        except ConnectionRefusedError:
            watchdog -= 1
        if watchdog == 0:
            break
        time.sleep(1)


def wait_until_down(watchdog):
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('127.0.0.1', 5000))
            s.close()
            watchdog -= 1
        except ConnectionRefusedError:
            break
        if watchdog == 0:
            break
        time.sleep(1)


@pytest.fixture()
def gameengineflask():
    proc = subprocess.Popen('src/gameengine.py')
    wait_until_up(5)
    yield "resource"
    proc.kill()
    wait_until_down(5)


def test_textclient_creation():
    tc = TextClient('localhost:5000')
    assert tc, "TextClient not created as expected"


def test_textclient_creation_with_http():
    tc = TextClient('http://localhost:5000')
    assert tc, "TextClient not created as expected"


def test_textclient_creation_bad_param():
    try:
        tc = TextClient('slocalhost')
        print(tc)
        assert False
    except ValueError:
        assert True


def test_tc_get_games(gameengineflask):
    tc = TextClient('localhost:5000')
    rc = tc.get_games_from_server()
    assert rc['status_code'] == 200


def test_tc_pick_random_key(gameengineflask):
    requests.post('http://localhost:5000/game_choice',
                  data='{"game_choice": "data/game_1.cfg"}')
    tc = TextClient('localhost:5000')
    rc = tc.get_key_data()
    assert rc.status_code == 200


def test_tc_send_valid_game_selection(gameengineflask):
    tc = TextClient('localhost:5000')
    rc = tc.send_game_selection_to_server('data/game_1.cfg')
    assert rc.status_code == 200, f'expected 200, got {rc.status_code}'
