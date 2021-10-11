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

    def process_rows(self, reader):
        """process_rows - process rows of CSV data and populate the keyboard
        """
        temp_row = list()
        cur_row = -1
        for row in reader:
            key = Key(*row)
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


def main():
    x = keyboard('English.csv')
    for row in x.read_config():
        if len(row):
            print(row[0])


if __name__ == "__main__":
    main()
