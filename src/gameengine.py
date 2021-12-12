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


class GameEngine(Flask):
    def __init__(self, application_name, config_file):
        super(GameEngine, self).__init__(application_name)
        self.config_file = config_file
        self.pingtime = 0
        self.data = {'game_config_path': None}
        self.game_chosen = None
        self.load_gameengine_config()
        self.setup_keyboards()
        self.add_endpoints()

    def add_endpoints(self):
        self.add_url_rule('/list_games',
                          view_func=self.list_game_handler_rule,
                          methods=['GET'])

        self.add_url_rule('/game_choice',
                          view_func=self.game_choice_rule,
                          methods=['GET', 'POST'])

        self.add_url_rule('/pick_key',
                          view_func=self.pick_key_rule,
                          methods=['GET'])

    def setup_keyboards(self):
        # self.player = KeyPlayer(self.data['host_kbd'],
        #                         self.data['target_kbd'])
        self.player = KeyPlayer('src/English.csv', 'src/Farsi_RTL.csv')

    def list_endpoints(self):
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
        target_char, host_char = self.player.from_target_pick_host()
        return {'target': target_char, 'host': host_char}, 200

    # from GET /listgames
    def list_game_handler_rule(self):
        files = glob(self.data['game_config_path'] + '/game_*.cfg')
        return str(files), 200

    # from GET | POST /gamechoice
    def game_choice_rule(self):
        method = request.method
        if method == 'GET':
            return str(self.game_chosen), 200
        elif method == 'POST':
            data = json.loads(request.get_data())
            self.game_chosen = data['game_choice']
            return 'OK', 200
        else:
            return 'Not Supported', 405


if __name__ == "__main__":
    x = GameEngine("game", "src/keyboarder.cfg")
    x.run()
