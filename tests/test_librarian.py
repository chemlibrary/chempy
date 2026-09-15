# tests/test_librarian.py

"""
Test script for librarian.py ledger integrity system
"""

import pytest
from ..librarian import make_ledger_file, verify_library
from ..files import file_safe_write, file_exists, file_delete, parent_path

@pytest.fixture
def ledger_creation():
    """Test ledger creation with sample files"""

    # Create ledger
    ledger_path = "./.librarian/ledger"
    make_ledger_file('.', str(ledger_path))

    # Verify ledger creation
    yield file_exists(ledger_path)

    file_delete('./.librarian/ledger')
    file_delete('./.librarian')

def test_ledger_creation(ledger_creation):
    assert ledger_creation == True


@pytest.fixture
def library_verification():
    """Test library verification after file modification"""

    # Create ledger
    ledger_path = "./.librarian/ledger"
    make_ledger_file('.', str(ledger_path))

    # Verify ledger creation
    assert file_exists(ledger_path)

    # Modify library and recheck
    testfile = './testlibfile.txt'
    file_safe_write(testfile, 'some contents')

    # Verify library
    yield verify_library()

    file_delete(testfile)
    file_delete('./.librarian/ledger')
    file_delete('./.librarian')

def test_library_verification(library_verification):
    assert library_verification == False


# Add more tests for edge cases, hash collision resistance, etc.