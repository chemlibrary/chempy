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

import secrets

def random_number(max_number:int = 100, min_number:int = 0, up_to:int = None):
    if up_to == None:
        max_number = max_number + 1
    else:
        max_number = up_to
    return secrets.randbelow(max_number - min_number) + min_number


def dice(rolls:int = 1, dice_type:str = None, dice_sides:int = 6, number_of_realities:int = 6) -> list[int]:
    if dice_type != None:
        dice_type = str(dice_type)
        if dice_type[0] == 'd':
            dice_type = dice_type[1:]
        if dice_type.isnumeric():
            dice_sides = int(dice_type)
    results = []
    for i in range(rolls):
        realities = []
        for x in range(number_of_realities):
            realities.append(random_number(min_number=1, max_number=dice_sides))
        reality_number = random_number(max_number=(len(realities) - 1))
        results.append(realities[reality_number])
    return results  
