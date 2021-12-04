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


def test_gameengine_creation():
    ge = GameEngine("Keyboarder")
    assert ge, 'Could not create GameEngine'


def test_gameengine_starts(gameengineflask):
    r = requests.get('http://localhost:5000/ping')
    assert r.status_code == 200
