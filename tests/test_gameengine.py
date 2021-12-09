import pytest
import subprocess
import requests
import time
from gameengine import GameEngine


@pytest.fixture()
def gameengineflask():
    proc = subprocess.Popen('src/gameengine.py')
    time.sleep(5)
    yield "resource"
    proc.kill()
    time.sleep(5)


def test_gameengine_creation():
    ge = GameEngine("Keyboarder", "src/keyboarder.cfg")
    assert ge, 'Could not create GameEngine'


def test_gameengine_starts(gameengineflask):
    r = requests.get('http://localhost:5000/ping')
    assert r.status_code == 200


def test_gameengine_postpingtime(gameengineflask):
    r = requests.post('http://localhost:5000/pingtime', data='{"data": 5}')
    assert r.status_code == 200


def test_list_games(gameengineflask):
    r = requests.get('http://localhost:5000/list_games')
    assert r.status_code == 200
    assert 'game_1.cfg' in r.text


def test_default_game_choice(gameengineflask):
    r = requests.get('http://localhost:5000/game_choice')
    assert r.status_code == 200


def test_set_game_choice(gameengineflask):
    r = requests.post('http://localhost:5000/game_choice',
                      data='{"game_choice": 3}')
    assert r.status_code == 200
    r = requests.get('http://localhost:5000/game_choice')
    assert r.status_code == 200
    assert r.text == '3'
