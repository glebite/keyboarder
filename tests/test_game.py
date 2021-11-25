from game import Game
from game import Label
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


def test_label():
    x = Label('this is a description', 25, 30)
    assert (25, 30, 'this is a description') == x.info()


def test_defaults_game_creation():
    x = Game('data/game_1.cfg')
    assert x.success == 0
    assert x.fail == 0
    assert x.first_time == 0
    assert x.last_time == 0


def test_load_game_duplicate_section():
    game = Game('data/game_test_duplicate_section.cfg')
    try:
        game.load_game()
        assert False, "Expected an exception here for bad data"
    except configparser.DuplicateSectionError:
        assert True


def test_load_game_duplicate_option():
    game = Game('data/game_test_duplicate_option.cfg')
    try:
        game.load_game()
        assert False, "Expected an exception here for bad data"
    except configparser.DuplicateOptionError:
        assert True


def test_start_clock_timed_set():
    game = Game('data/game_3.cfg')
    game.load_game()
    first = game.first_time
    started = game.start_clock()
    assert first == 0 and started != 0


def test_start_clock_timed_not_set():
    game = Game('data/game_1.cfg')
    game.load_game()
    first = game.first_time
    started = game.start_clock()
    assert first == 0 and started == 0


def test_stop_clock_timed_set():
    game = Game('data/game_3.cfg')
    game.load_game()
    last = game.first_time
    started = game.stop_clock()
    assert last == 0 and started != 0


def test_stop_clock_timed_not_set():
    game = Game('data/game_1.cfg')
    game.load_game()
    last = game.first_time
    started = game.start_clock()
    assert last == 0 and started == 0
