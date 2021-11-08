"""
"""
from key import Key
import csv
import random


class Keyboard(object):
    """Keyboard - collection of keys for a given keyboard
    """
    def __init__(self, key_file):
        """
        """
        self.key_file = key_file
        self.layout = list()
        self.position = dict()
        self.pos_map = dict()
        self.rows = 0

    def process_rows(self, reader):
        """process_rows - process rows of CSV data and populate the keyboard

        Params:
        reader - CSVReader - used to retrieve lines

        Returns:
        n/a

        Raises:
        n/a
        """
        temp_row = list()
        cur_row = 0
        for row in reader:
            key = Key(*row)
            self.position[key.upper] = (key.row, key.column)
            self.position[key.lower] = (key.row, key.column)
            self.pos_map[(key.row, key.column)] = [key.lower, key.upper]

            # This is what is killing me - losing first key really...
            if key.row != cur_row:
                self.layout.append(temp_row)
                temp_row = [key]
                cur_row = key.row
            else:
                temp_row.append(key)
        self.layout.append(temp_row)
        self.rows = key.row

    def read_config(self):
        """read_config - read a keyboard file and process the data
        """
        with open(self.key_file, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',',
                                quotechar="\'",
                                skipinitialspace=True,
                                doublequote=False,
                                quoting=csv.QUOTE_NONNUMERIC)
            self.process_rows(reader)

    def get_key_position(self, character):
        """get_key_position
        """
        if character in self.position:
            return self.position[character]
        else:
            return (-1, -1)

    def get_char_from_position(self, row, column):
        """get_char_from_position
        """
        return self.pos_map[(row, column)]

    def pick_random_key(self):
        flat_list = [item for sublist in self.layout for item in sublist]
        return random.choice(flat_list).lower


if __name__ == "__main__":
    x = Keyboard('Farsi_RTL.csv')
    x.read_config()
    for key in x.layout[3]:
        print(key.lower)
