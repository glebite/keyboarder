class Key(object):
    """Key - definition of a Key class.

    This will allow for the addressing of a key based on 
    its row, column, whether or not it should be displayed, or what
    to display when it's either upper case or lower case.
    """
    def __init__(self, row, column, visibility, cases):
        """__init__ - constructor

        Params:
        row - int - keyboard row (0 < row < n)
        column - int - keyboard column (0 < column < m)
        visibility - int - whether or not the key is to be displayed
        cases - dict:
                {'lower' : 'a',
                 'upper' : 'A'}
        Returns:
        n/a

        Raises:
        n/a
        """
        assert 0 < row < 25, f'{row} out of 0<row<25 bounds'
        assert 0 < column < 80, f'{column} out of 0<column<25 bounds'
        self.row = row
        self.column = column
        self.visibility = visibility
        self.cases = cases

    def __str__(self):
        return f'{self.row} {self.column} {self.visibility} {self.cases}'


def main():
    try:
        x = Key(39, 10, 1, {'lower': 'a', 'upper': 'A'})
        print(f'{x}')
    except AssertionError as e:
        print(f'Caught expected exception {e}')
    x = Key(10, 10, 1, {'lower': 'a', 'upper': 'A'})
    print(f'{x}')


if __name__ == "__main__":
    main()
