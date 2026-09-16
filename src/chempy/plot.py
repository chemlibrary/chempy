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

import math

def points_in_circle(center, diameter):
	radius = diameter/2
	points = []

	x_min = center[0] - radius
	x_max = center[0] + radius
	y_min = center[1] - radius
	y_max = center[1] + radius

	for x in range(int(x_min), int(x_max) +1):
		for y in range(int(y_min), int(y_max)+1):
			distance = math.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2)
			if distance <= radius:
				points.append(x, y)
	return points


def shift_point(x, y, angle_degrees, distance):
	angle_radians = math.radians(angle_degrees)
	new_x = x + distance * math.cos(angle_radians)
	new_y = y + distance * math.sin(angle_radians)
	return new_x, new_y
