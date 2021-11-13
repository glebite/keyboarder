import csv
import glob


LOCATION = './src/*.csv'


def test_confirm_CSV_files_exist():
    files_to_check = glob.glob(LOCATION)
    assert files_to_check, f'No .csv files defined in {LOCATION}'


def test_confirm_CSV_file_integrity():
    files_to_check = glob.glob(LOCATION)
    for csv_file in files_to_check:
        with open(csv_file, newline='\n') as csvfile:
            output = csv.DictReader(csvfile)
            num_fieldnames = len(output.fieldnames)
            assert num_fieldnames == 5, \
                f'Expected 5 fieldnames and got {num_fieldnames}'
