import pytest
import subprocess
import requests
import time
import configparser
from gameengine import GameEngine
import socket


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


def test_gameengine_creation():
    ge = GameEngine("Keyboarder", "src/keyboarder.cfg")
    assert ge, 'Could not create GameEngine'


def test_list_games(gameengineflask):
    r = requests.get('http://localhost:5000/list_games')
    assert r.status_code == 200
    assert 'game_1.cfg' in r.text


def test_default_game_choice(gameengineflask):
    r = requests.get('http://localhost:5000/game_choice')
    assert r.status_code == 200


def test_set_game_choice(gameengineflask):
    r = requests.post('http://localhost:5000/game_choice',
                      data='{"game_choice": "data/game_1.cfg"}')
    assert r.status_code == 200
    r = requests.get('http://localhost:5000/game_choice')
    assert r.status_code == 200
    assert r.text == 'data/game_1.cfg'


def test_gameengine_config_does_not_exist():
    try:
        GameEngine('name', '../data/game_doesnotexist.cfg')
        assert False
    except FileNotFoundError:
        assert True


def test_game_invalid_config_file():
    try:
        GameEngine('name', 'README.md')
        assert False, "README.md is not a config file and should have" \
            " thrown an exception - MissingSectionHeaderError."
    except configparser.MissingSectionHeaderError:
        assert True


def test_gameengine_bad_method_choice(gameengineflask):
    r = requests.delete('http://localhost:5000/game_choice')
    assert r.status_code == 405


def test_url_endpoint_creations():
    ge = GameEngine("Keyboarder", "src/keyboarder.cfg")
    endpoints = ge.list_endpoints()
    assert 'game_choice' in str(endpoints)


def test_pick_random_key(gameengineflask):
    requests.post('http://localhost:5000/game_choice', data='{"game_choice": "data/game_1.cfg"}')
    r = requests.get('http://localhost:5000/pick_key')
    assert r.status_code == 200


def test_default_scores():
    ge = GameEngine("Keyboarder", "src/keyboarder.cfg")
    scores = ge.scores
    assert scores['success'] == 0 and scores['fail'] == 0


def test_increment_success():
    ge = GameEngine("Keyboarder", "src/keyboarder.cfg")
    scores = ge.scores
    assert scores['success'] == 0 and scores['fail'] == 0
    ge.increment_result('success')
    assert scores['success'] == 1 and scores['fail'] == 0


def test_clear_scores():
    ge = GameEngine("Keyboarder", "src/keyboarder.cfg")
    ge.increment_result('success')
    scores = ge.scores
    assert scores['success'] == 1 and scores['fail'] == 0
    ge.clear_results()
    scores = ge.scores
    assert scores['success'] == 0 and scores['fail'] == 0


def test_basic_reset_status():
    ge = GameEngine("Keyboarder", "src/keyboarder.cfg")
    ge.game_status['current_stage'] = 3
    assert ge.game_status['current_stage'] == 3
    ge.reset_game_status()
    assert ge.game_status['current_stage'] == 0


def test_all_values_reset_status():
    ge = GameEngine("Keyboarder", "src/keyboarder.cfg")
    ge.scores = {'fail': 1, 'success': 2}
    ge.game_status['scores'] = ge.scores
    ge.game_status['current_stage'] = 3
    ge.game_status['remaining'] = 4

    assert ge.game_status['scores']['fail'] == 1
    assert ge.game_status['scores']['success'] == 2
    assert ge.game_status['current_stage'] == 3
    assert ge.game_status['remaining'] == 4

    ge.reset_game_status()
    assert ge.game_status['scores']['fail'] == 0
    assert ge.game_status['scores']['success'] == 0
    assert ge.game_status['current_stage'] == 0
    assert ge.game_status['remaining'] == 0
