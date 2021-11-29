from game import Game
from game import Label
from keyplayer import KeyPlayer
import configparser
import time
import curses
import pytest


@pytest.fixture(autouse=True)
def shutdown_screen():
    yield
    try:
        curses.endwin()
    except curses.error:
        pass


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


def test_configure_game_missing_option():
    game = Game('data/game_test_missing_option.cfg')
    assert game.load_game() is False


def test_configure_game_extra_option():
    game = Game('data/game_test_extra_option.cfg')
    try:
        game.load_game()
        assert False
    except KeyError:
        assert True


def test_update_time_defaults():
    game = Game('data/game_3.cfg')
    game.load_game()
    assert game.update_time('a') == 0


def test_update_time_normal():
    game = Game('data/game_3.cfg')
    game.load_game()
    game.start_clock()
    time.sleep(1)
    game.stop_clock()
    assert game.update_time('a') >= 1


def test_update_score_success():
    game = Game('data/game_3.cfg')
    game.load_game()
    game.update_score('a', 'a', 'A')
    assert game.success == 1


def test_update_score_failure():
    game = Game('data/game_3.cfg')
    game.load_game()
    game.update_score('a', 'b', 'B')
    assert game.fail == 1
    assert game.failed_characters == ['B']


def test_bring_up_screen():
    game = Game('data/game_3.cfg')
    game.load_game()
    game.player = KeyPlayer('src/'+game.data['host_kbd'],
                            'src/'+game.data['target_kbd'])
    game.setup_display()
    game.player.host_layout.screen_deinit()


def test_bring_up_current_word():
    game = Game('data/game_5.cfg')
    game.load_game()
    game.player = KeyPlayer('src/'+game.data['host_kbd'],
                            'src/'+game.data['target_kbd'])
    game.setup_display()
    screen = game.player.host_layout.screen_dump()
    expected = "Current word:"
    for i, value in enumerate(expected, start=55):
        read_value = screen[f'4,{i}']
        assert ord(value) == read_value, f'Read: {read_value}'\
            f' ({chr(read_value)}) expecting:'\
            f' {ord(value)} ({value}) for {i}'
    game.player.host_layout.screen_deinit()


def test_hinting_on():
    game = Game('data/game_1.cfg')
    game.load_game()
    game.player = KeyPlayer('src/'+game.data['host_kbd'],
                            'src/'+game.data['target_kbd'])
    game.setup_display()
    game.hint_on('1')
    screen = game.player.host_layout.screen_dump()
    expected = ord('1')
    value = screen['1,4']
    expected = ord('1') | curses.A_STANDOUT
    assert value == expected, f'Expected {expected}, got {value} instead.'
    game.player.host_layout.screen_deinit()


def test_key_hint_off():
    game = Game('data/game_1.cfg')
    game.load_game()
    game.player = KeyPlayer('src/'+game.data['host_kbd'],
                            'src/'+game.data['target_kbd'])
    game.setup_display()
    game.hint_on('1')
    game.hint_off('1')
    screen = game.player.host_layout.screen_dump()
    value = screen['1,4']
    expected = ord('1')
    assert value == expected, f'Expected {expected}, got {value} instead.'
    game.player.host_layout.screen_deinit()


def test_update_score_display():
    game = Game('data/game_5.cfg')
    game.load_game()
    game.player = KeyPlayer('src/'+game.data['host_kbd'],
                            'src/'+game.data['target_kbd'])
    game.setup_display()

    game.fail = 5
    game.success = 3
    game.update_score_display()
    screen = game.player.host_layout.screen_dump()

    expected = "3"
    read_value = screen['8,65']
    assert chr(read_value) == expected
    expected = "5"
    read_value = screen['9,65']
    assert chr(read_value) == expected
    game.player.host_layout.screen_deinit()


def test_print_results_no_fails(capsys):
    game = Game('data/game_1.cfg')
    game.load_game()
    game.player = KeyPlayer('src/'+game.data['host_kbd'],
                            'src/'+game.data['target_kbd'])
    game.success = 20
    game.fail = 0
    captured = capsys.readouterr()
    game.print_results()
    print(f'Output: {captured.out}')
    
