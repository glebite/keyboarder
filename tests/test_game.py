from game import Game


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
