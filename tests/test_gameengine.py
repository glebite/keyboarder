import pytest
import subprocess
import requests
import time
import configparser
from gameengine import GameEngine


@pytest.fixture()
def gameengineflask():
    proc = subprocess.Popen('src/gameengine.py')
    time.sleep(1)
    yield "resource"
    proc.kill()
    time.sleep(1)


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
                      data='{"game_choice": 3}')
    assert r.status_code == 200
    r = requests.get('http://localhost:5000/game_choice')
    assert r.status_code == 200
    assert r.text == '3'


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
