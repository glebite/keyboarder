"""
kboard.py

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

        params:
        reader - CSVReader - used to retrieve lines

        returns:
        n/a

        raises:
        n/a
        """
        temp_row = list()
        cur_row = 0
        for row in reader:
            key = Key(*row)
            self.position[key.upper] = (key.row, key.column)
            self.position[key.lower] = (key.row, key.column)
            self.pos_map[(key.row, key.column)] = [key.lower, key.upper]

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
        """get_key_position - return the row, col location of the character
        """
        if character in self.position:
            return self.position[character]
        else:
            return (-1, -1)

    def get_char_from_position(self, row, column):
        """get_char_from_position - find character based on row, column
        """
        return self.pos_map[(row, column)]

    def pick_random_key(self):
        """pick_random_key - find a random key from the list of available keys
        """
        # TODO: extract this from the keys
        remove_list = ['TAB', 'CAPS', 'SHIFT']
        flat_list = [item for sublist in self.layout for item in sublist
                     if item.lower not in remove_list]
        
        choice = random.choice(flat_list)
        flat_list.remove(choice)
        return choice.lower
