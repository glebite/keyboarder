import requests


class TextClient:
    def __init__(self, server_ip):
        if ':' not in server_ip:
            raise ValueError
        self.server_ip = server_ip
