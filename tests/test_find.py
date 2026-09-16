import pytest
import os

from chempy.find import find_in_file, find_numbers_in_file_by_length, find_numbers_in_string_by_length
from chempy.files import parent_path

def test_find_in_file():
    # Test finding a string in a file
    file_path = f'{parent_path(os.path.abspath(__file__))}{os.sep}resources/test1.txt'
    results = find_in_file('import', file_path)
    assert len(results) >= 1  # Should find at least one 'import' statement

    # Test non-existent file
    with pytest.raises(FileNotFoundError):
        find_in_file('test', 'invalid_file.py')

    # Test empty search string
    results = find_in_file('', file_path)
    assert len(results) == 0  # Empty string should return no matches


def test_find_numbers_in_file_by_length():
    # Test finding 3-digit numbers in a file
    file_path = f'{parent_path(os.path.abspath(__file__))}{os.sep}resources/test1.txt'
    results = find_numbers_in_file_by_length(3, file_path)
    assert len(results) >= 1  # Should find at least one 3-digit numbers

    # Test invalid file
    with pytest.raises(FileNotFoundError):
        find_numbers_in_file_by_length(3, 'invalid_file.py')

    # Test zero-length numeric string
    results = find_numbers_in_file_by_length(0, file_path)
    assert len(results) == 0


def test_find_numbers_in_string_by_length():
    # Test finding 3-digit numbers in a string
    test_string = 'abc123def456ghi789jkl'
    results = find_numbers_in_string_by_length(3, test_string)
    assert results == ['123', '456', '789']

    # Test non-numeric string
    results = find_numbers_in_string_by_length(3, 'abcdefg')
    assert len(results) == 0

    # Test edge case: number at end of string
    results = find_numbers_in_string_by_length(3, 'abc123')
    assert results == ['123']