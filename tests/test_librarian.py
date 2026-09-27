# This file is part of ChemPy.
# Copyright (C) 2026 Chem
#
# ChemPy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ChemPy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ChemPy. If not, see <http://www.gnu.org/licenses/>.

# tests/test_librarian.py

"""
Test script for librarian.py ledger integrity system
"""

import pytest
from chempy.librarian import make_ledger_file, verify_library
from chempy.files import file_safe_write, file_exists, file_delete, parent_path

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

