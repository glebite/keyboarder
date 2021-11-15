from game import Game
import configparser


def test_game_creation():
    game = Game('../data/game_1.cfg')
    if not game:
        assert False


def test_game_valid_config():
    game = Game('data/game_1.cfg')
    try:
        game.load_game()
        assert True
    except FileNotFoundError:
        assert False


def test_game_missing_config():
    game = Game('../data/game_123.cfg')
    try:
        game.load_game()
        assert False
    except FileNotFoundError:
        assert True


def test_game_invalid_config_file():
    game = Game('README.md')
    try:
        game.load_game()
        assert False, "README.md is not a config file and should have" \
            " thrown an exception - MissingSectionHeaderError."
    except configparser.MissingSectionHeaderError:
        assert True


def test_load_game():
    game = Game('data/game_1.cfg')
    game.load_game()
    assert game.data['target_kbd'] == 'Farsi_RTL.csv', f"target_kbd" \
        f" is {game.data['target_kbd']} instead of Farsi_RTL.csv"
