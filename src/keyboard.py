from key import Key
import csv


class keyboard(object):
    def __init__(self, key_file):
        self.key_file = key_file
        self.layout = list()

    def read_config(self):
        temp_row = list()
        cur_row = -1
        with open(self.key_file, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='\'')
            for row in reader:
                # retrieve row and column info - well all data
                # if cur_row != row
                #    self.layout.append(temp_row)
                #    cur_row = row
                print(row)
                x = Key(*row)
                print(x)


def main():
    x = keyboard('English.csv')
    x.read_config()


if __name__ == "__main__":
    main()
