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


def parse_conf_file(path):
    """
    Parse a simple Linux .conf file into a dictionary.
    """
    config = {}

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            # Skip blank lines and comments
            if not line or line.startswith("#"):
                continue

            # Only process lines containing '='
            if "=" not in line:
                continue

            key, value = line.split("=", 1)
            config[key.strip()] = value.strip()

    return config

if __name__ == '__main__':
    print(parse_conf_file('/home/user/Desktop/test/test.conf'))