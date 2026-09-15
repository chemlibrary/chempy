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
