"""
"""
from key import Key
import csv


class keyboard(object):
    """
    """
    def __init__(self, key_file):
        """
        """
        self.key_file = key_file
        self.layout = list()
        self.position = dict()
        self.pos_map = dict()

    def process_rows(self, reader):
        """process_rows - process rows of CSV data and populate the keyboard
        """
        temp_row = list()
        cur_row = -1
        for row in reader:
            print(row)
            key = Key(*row)
            self.position[key.upper] = (key.row, key.column)
            self.position[key.lower] = (key.row, key.column)
            self.pos_map[(key.row, key.column)] = {key.lower, key.upper}
            
            if key.row != cur_row:
                self.layout.append(temp_row)
                temp_row = list()
                cur_row = key.row
            else:
                temp_row.append(key)
        self.layout.append(temp_row)

    def read_config(self):
        """
        """
        with open(self.key_file, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='\'')
            self.process_rows(reader)

    def get_key_position(self, character):
        return self.position[character]

    def get_char_from_position(self, row, column):
        return self.pos_map[(row, column)]


def main():
    x = keyboard('Farsi.csv')
    x.read_config()

    print(x.get_key_position('ت'))
    print(x.get_char_from_position(3, 3))


if __name__ == "__main__":
    main()
