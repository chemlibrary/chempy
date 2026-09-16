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

def get_grayscales() -> list[str]:

    # This scale is good for higher resolution images:
    scales = ['@&%QWNM0gB$#DR8mHXKAUbGOpV4d9h6PkqwSE2]ayjxY5Zoen[ult13If}C{iF|(7J)vTLs?z/*cr!+<>;=^_:\'-.` ']

    # 8-bit:
    scales.append('MNFVI$*:.')

    # 32-bit
    scales.append('MWNQBHKR#EDFXOAPGUSVZYCLTJ$I*:. ')

    # This charset may not be the best choice on many systems:
    scales.append('$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,"^.`\'')

    # 1997 "Standard" character ramp by Paul Bourke:
    scales.append('$@B%8&WM#*oahkdbpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,"^`\'.')

    return scales


def ascii_grayscale(scale_number:int = 0, reverse_scale:bool = False):

    # get list of avaiable grayscales
    scales = get_grayscales()

    # sanity check:
    if scale_number > len(scales):
        scale_number = 0

    scale = scales[scale_number]

    if reverse_scale:
        scale_characters = list(scale)
        reversed_characters = scale_characters[::-1]
        scale = ''.join(reversed_characters)

    return scale
