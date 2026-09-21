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

## Sticky booleans that can only be changed once.
class Sbool:
    def __init__(self, b:bool = True):
        self.__b = b
        self.__x = not(b)
    def __str__(self):
        return str(self.__b)
    def __repr__(self):
        return str(self.__b)
    def __bool__(self):
        return bool(self.__b)
    def __eq__(self, other):
        return self.__b == other
    def __ne__(self, other):
        return self.__b != other
    def value(self):
        return self.__b
    def locked(self) -> bool:
        return self.__b == self.__x
    def flip(self) -> bool:
        if not self.locked():
            self.__b = self.__x
            return True
        return False
    def set(self, target):
        if self.value() != target:
            self.flip()
        return self.value()
