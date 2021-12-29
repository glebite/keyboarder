#!/usr/bin/env python3
# so how well will this work in windows?  Sigh...
from flask import Flask
from flask import request
import json
import configparser
from configparser import DuplicateSectionError, DuplicateOptionError
from ast import literal_eval
from glob import glob
from keyplayer import KeyPlayer
import sys


class GameEngine(Flask):
    def __init__(self, application_name, config_file):
        """__init__
        """
        super(GameEngine, self).__init__(application_name)
        self.config_file = config_file
        self.pingtime = 0
        self.data = {'game_config_path': None}
        self.game_chosen = None
        self.load_gameengine_config()
        self.add_endpoints()
        self.scores = {'success': 0, 'fail': 0}
        self.game_data = {'name': None,
                          'description': None,
                          'characters': None,
                          'timed': None,
                          'hints': None,
                          'number': None,
                          'words': None,
                          'word_file': None,
                          'host_kbd': None,
                          'target_kbd': None}

    def add_endpoints(self):
        """add_endpoints - register endpoints here
        """
        self.add_url_rule('/list_games',
                          view_func=self.list_game_handler_rule,
                          methods=['GET'])

        self.add_url_rule('/game_choice',
                          view_func=self.game_choice_rule,
                          methods=['GET', 'POST'])

        self.add_url_rule('/pick_key',
                          view_func=self.pick_key_rule,
                          methods=['GET'])

        self.add_url_rule('/get_score',
                          view_func=self.get_score_rule,
                          methods=['GET'])

        self.add_url_rule('/get_info',
                          view_func=self.get_info_rule,
                          methods=['GET'])

    def setup_keyboards(self):
        self.player = KeyPlayer(self.game_data['host_kbd'],
                                self.game_data['target_kbd'])

    def list_endpoints(self):
        """list_endpoints"""
        return self.url_map

    def load_gameengine_config(self):
        """load_game - method for loading the game config file

        params:
        n/a

        returns:
        True/False - bool based on whether the game config could load

        raises:
        FileNotFoundError if the config file is not found
        DuplicateSectionError if a duplicate section is in the config file
        DuplicateOptionError if there is a duplicate option in the config file
        """
        try:
            self.cfg_parser = configparser.\
                ConfigParser(converters={"any": lambda x: literal_eval(x)})
            self.cfg_parser.read_file(open(self.config_file, 'r'))
            return self._configure_gameengine()
        except FileNotFoundError:
            raise FileNotFoundError
        except DuplicateSectionError as e:
            raise e
        except DuplicateOptionError as e:
            raise e

    def _configure_gameengine(self):
        """_configure_game - assign tables/variables

        Note: int values get converted from strings
              booleans get converted from strings
        """
        for entry in self.cfg_parser['GameEngine']:
            if entry not in self.data.keys():
                raise KeyError
            if self.cfg_parser['GameEngine'][entry].isdigit():
                self.data[entry] =\
                    int(self.cfg_parser['GameEngine'][entry])
            elif self.cfg_parser['GameEngine'][entry] in ['True', 'False']:
                self.data[entry] =\
                    bool(self.cfg_parser['GameEngine'][entry] == 'True')
            else:
                self.data[entry] =\
                    self.cfg_parser['GameEngine'][entry]

        return None not in self.data.values()

    def pick_key_rule(self):
        """ pick_key_rule """
        target_char, host_char = self.player.from_target_pick_host()
        return {'target': target_char, 'host': host_char}, 200

    # from GET /listgames
    def list_game_handler_rule(self):
        files = glob(self.data['game_config_path'] + '/game_*.cfg')
        return {'status_code': 200, 'game_list': list(files)}

    # from GET | POST /gamechoice
    def game_choice_rule(self):
        method = request.method
        if method == 'GET':
            return str(self.game_chosen), 200
        elif method == 'POST':
            data = json.loads(request.get_data())
            self.game_chosen = data['game_choice']
            # import pdb; pdb.set_trace()
            self.get_game_configuration()
            self.setup_keyboards()
            return 'OK', 200
        else:
            return 'Not Supported', 405

    def load_game(self):
        """load_game - method for loading the game config file

        params:
        n/a

        returns:
        True/False - bool based on whether the game config could load

        raises:
        FileNotFoundError if the config file is not found
        DuplicateSectionError if a duplicate section is in the config file
        DuplicateOptionError if there is a duplicate option in the config file
        """
        self.cfg_parser = configparser.\
            ConfigParser(converters={"any": lambda x: literal_eval(x)})
        try:
            self.cfg_parser.read_file(open(self.game_file, 'r'))
        except FileNotFoundError:
            print(f'Sorry - file not found... {self.game_file}')
            raise FileNotFoundError
        except DuplicateSectionError as e:
            raise e
        except DuplicateOptionError as e:
            raise e

        return self._configure_game()

    def _configure_game(self):
        """_configure_game - assign tables/variables

        Note: int values get converted from strings
              booleans get converted from strings
        """
        for entry in self.cfg_parser['Game']:
            if entry not in self.game_data.keys():
                raise KeyError
            if self.cfg_parser['Game'][entry].isdigit():
                self.game_data[entry] =\
                    int(self.cfg_parser['Game'][entry])
            elif self.cfg_parser['Game'][entry] in ['True', 'False']:
                self.game_data[entry] =\
                    bool(self.cfg_parser['Game'][entry] == 'True')
            else:
                self.game_data[entry] =\
                    self.cfg_parser['Game'][entry]

        return None not in self.game_data.values()

    def get_game_configuration(self):
        self.game_file = self.game_chosen
        self.load_game()

    def increment_result(self, result):
        self.scores[result] += 1

    def clear_results(self):
        self.scores = {'success': 0, 'fail': 0}

    def get_score_rule(self):
        return str(self.scores), 200

    def get_info_rule(self):
        return {'status_code': 200, 'data':
                {'config_file': self.config_file,
                 'pingtime': self.pingtime,
                 'data': self.data,
                 'game_data': self.game_data,
                 'game_chosen': self.game_chosen,
                 'scores': self.scores}}


if __name__ == "__main__":
    if len(sys.argv) == 2:
        config_file = sys.argv[1]
    else:
        config_file = 'src/keyboarder.cfg'
    game_engine = GameEngine("game", config_file)
    game_engine.run()
