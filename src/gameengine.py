#!/usr/bin/env python3
# so how well will this work in windows?  Sigh...
import flask


class GameEngine(flask.Flask):
    def __init__(self, application_name):
        super(GameEngine, self).__init__(application_name)
        self.add_url_rule('/ping',
                          view_func=self.ping,
                          methods=['GET'])

    def ping(self):
        return 'pong'


if __name__ == "__main__":
    x = GameEngine("game")
    x.run()
