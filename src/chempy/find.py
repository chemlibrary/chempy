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

import re
from .files import file_read


def find_in_file(search:str, file_path:str) -> list[int]:
    # find all occurences of a string in a file
    results = []
    if search == '' or search == None:
        return results
    contents = file_read(file_path)
    if contents != None:
        results = [m.start() for m in re.finditer(search, contents)]
    # return a list of positions of the first character of each match
    return results


def find_numbers_in_file_by_length(length:int, file_path:str) -> list[str]:
    # find all numeric substrings with the specified length
    results = []
    contents = file_read(file_path)
    if contents != None:
        results = find_numbers_in_string_by_length(length, contents)
    # return a list of the matching numbers
    return results


def find_numbers_in_string_by_length(length: int, string_to_search: str) -> list[str]:
    # find all numeric substrings with the specified length
    results = []
    for i in range(len(string_to_search)):
        # Check if the current character is numeric
        if string_to_search[i].isnumeric():
            # Extract the substring of the specified length
            substring = string_to_search[i:i+length]
            if substring.isnumeric():
                # Check if the next character (if it exists) is not numeric
                next_char = string_to_search[i + length] if (i + length) < len(string_to_search) else None
                # Check if the previous character (if it exists) is not numeric
                prev_char = string_to_search[i - 1] if (i - 1) >= 0 else None
                # Ensure the substring is surrounded by non-numeric characters
                if (next_char is None or not next_char.isnumeric()) and (prev_char is None or not prev_char.isnumeric()):
                    results.append(substring)
    return results
