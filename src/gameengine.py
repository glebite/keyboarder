#!/usr/bin/env python3
# so how well will this work in windows?  Sigh...
from flask import Flask
from flask import request
import json


class GameEngine(Flask):
    def __init__(self, application_name):
        super(GameEngine, self).__init__(application_name)
        self.pingtime = 0

        self.add_url_rule('/ping', view_func=self.ping_handler,
                          methods=['GET'])

        self.add_url_rule('/pingtime',
                          view_func=self.pingtime_handler,
                          methods=['POST'])

    def ping_handler(self):
        return f'pong is {self.pingtime}'

    def pingtime_handler(self):
        data = json.loads(request.get_data())
        self.pingtime = data['data']
        return f'pong changed now to {self.pingtime}'


if __name__ == "__main__":
    x = GameEngine("game")
    x.run()
