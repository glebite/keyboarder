#!/usr/bin/env python3
# so how well will this work in windows?  Sigh...
from flask import Flask
from flask import request
import json
import configparser
from configparser import DuplicateSectionError, DuplicateOptionError
from ast import literal_eval
from glob import glob


class GameEngine(Flask):
    def __init__(self, application_name, config_file):
        super(GameEngine, self).__init__(application_name)
        self.config_file = config_file
        self.pingtime = 0
        self.data = {'game_config_path': None}
        self.load_game()
        
        self.add_url_rule('/ping', view_func=self.ping_handler,
                          methods=['GET'])

        self.add_url_rule('/pingtime',
                          view_func=self.pingtime_handler,
                          methods=['POST'])

        self.add_url_rule('/list_games',
                          view_func=self.list_game_handler,
                          methods=['GET'])

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
            self.cfg_parser.read_file(open(self.config_file, 'r'))
        except FileNotFoundError:
            print(f'Sorry - file not found... {self.config_file}')
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

    def ping_handler(self):
        return f'pong is {self.pingtime}'

    def pingtime_handler(self):
        data = json.loads(request.get_data())
        self.pingtime = data['data']
        return f'pong changed now to {self.pingtime}'

    def list_game_handler(self):
        files = glob(self.data['game_config_path'] + '/game_*.cfg')
        return str(files)


if __name__ == "__main__":
    x = GameEngine("game", "./keyboarder.cfg")
    x.run()
