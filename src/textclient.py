import requests
import sys


class TextClient:
    def __init__(self, server_ip):
        if ':' not in server_ip:
            raise ValueError
        self.server_ip = server_ip
        self.player = None

    def get_key_data(self):
        r = requests.get(self.server_ip + '/pick_key')
        print(r.status_code)

       
if __name__ == "__main__":
    tc = TextClient(sys.argv[1])
    tc.get_key_data()
