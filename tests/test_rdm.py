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

from chempy.rdm import (
    random_number,
    dice,
)


## Smoke Tests

def test_random_number():
    number = random_number()
    assert isinstance(number, int)

def test_dice():
    roll = dice()
    assert isinstance(roll[0], int)


## Functional Tests

def test_dice_dice_sides_and_rolls():
    rolls = dice(rolls=5, dice_sides=6)
    assert len(rolls) == 5
    assert isinstance(rolls[0], int)

def test_dice_dice_type_and_rolls():
    rolls = dice(5, 'd6')
    assert len(rolls) == 5
    isinstance(rolls[0], int)