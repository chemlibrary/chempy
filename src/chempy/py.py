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

import os
from chempy.files import parent_path, file_name, file_extension, file_safe_write


def create_package_toml(package_name:str, target_dir:str = None, description:str = "", author:str = "", email:str = "", license:str = "GPL-3.0-or-later", homepage:str = ""):
    if target_dir == None:
        target_dir = f".{os.sep}"
    contents = f"""[build-system]
requires = ["setuptools>=77"]
build-backend = "setuptools.build_meta"

[project]
name = "{package_name}"
version = "2.1.6"
authors = [
  {{ name="{author}", email="{email}" }},
]
description = "{description}"
readme = "README.md"
requires-python = ">=3.9"
classifiers = [
    "Programming Language :: Python :: 3",
    "Operating System :: OS Independent",
]
license = "{license}"
license-files = ["LICEN[CS]E*"]

[project.urls]
Homepage = "{homepage}"

[tool.setuptools.packages.find]
where = ["src"]

"""
    try:
        return file_safe_write(f"{target_dir}{os.sep}pyproject.toml", contents = contents)
    except:
        return False


def detect_indentation(path:str) -> int:
    try:
        with open(path, 'r') as file:
            lines = file.readlines()
        whitespace_count = 0
        for line in lines:
            ## Identify the indentation by counting leading whitespace
            leading_whitespace = len(line) - len(line.lstrip(' '))
            if leading_whitespace > 0:
                if whitespace_count == 0:
                    whitespace_count = leading_whitespace
                elif whitespace_count != leading_whitespace:
                    print(f"Warning: Mixed indentation found - {leading_whitespace} whitespaces on a line with {whitespace_count} whitespaces.")
                    return
                ## Stop counting after finding the first indent
                break
        if whitespace_count > 0:
            return whitespace_count
        else:
            return None
    except FileNotFoundError:
        print("The specified file does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return None

if __name__ == '__main__':
    print(create_package_toml('test-package','/home/user/Desktop','test description','test author', 'test@email.com',))