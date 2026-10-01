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

## List functions for more readable source code

from chempy.rdm import random_number
import random


def reverse_list(li):
    return li[::-1]


def string_to_list(str):
    return list(str)


def list_to_string(list):
    return ''.join(list)


def shuffle_list(unshuffled:list):
    random.seed(random_number(up_to=1000000000))
    shuffled = unshuffled
    random.shuffle(shuffled)
    return shuffled
