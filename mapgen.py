import math

import svgwrite as svg
import config

class Point(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __getitem__(self, index):
		if index == 0: return self.x
		if index == 1: return self.y
		raise IndexError()

	def __str__(self):
		return "({}, {})".format(self.x, self.y)

	def __add__(self, other):
		return Point(self.x + other.x, self.y + other.y)

	def __neg__(self):
		return Point(-self.x, -self.y)

	def __sub__(self, other):
		return self + (-other)

	def __mul__(self, other):
		if isinstance(other, float) or isinstance(other, int):
			return Point(self.x*other, self.y*other)
		raise NotImplementedError()

mapsize = (450, 200)

position = Point(230, 75)
bearing_pos = Point(195., 155.)
time_pos = Point(300., 100.)
target_pos = Point(330.,  30.)

antenna_resolution = 180

grid = True

def convert_angle_to_antenna(angle):
	while angle < 0:
		angle += 360
	while angle >= 360:
		angle -= 360
	return round(angle/360*antenna_resolution)

s = svg.Drawing("output/map.svg", width=4500, height=2000)

# markers
city05 = s.symbol()
city05.add(s.circle(center=(0, 0), r=2, stroke="black", fill="white"))
s.add(city05)

city10 = s.symbol()
city10.add(s.circle(center=(0, 0), r=2, stroke="black", fill="red"))
s.add(city10)

city25 = s.symbol()
city25.add(s.rect(insert=(-2, -2), size=(4, 4), stroke="black", fill="red"))
s.add(city25)

base00 = s.symbol()
base00.add(s.polygon(points=(
	(-2, 2),
	( 0,-2),
	( 2, 2)
	), stroke="black", fill="white"))
s.add(base00)

# styles
s.defs.add(s.style(".location { font-size: 4px; alignment-baseline: middle; } .grid { stroke-width: 0.3px; stroke: gray; }"))


markers = [
	(target_pos.x,  target_pos.y, city10, 1200000, "?", "spotlight", ""),
	(time_pos.x, time_pos.y, city10, 1400000, "Perengard", "lollipop", ""),
	(200., 165., city10, 1800000, "Darvenhoff", "siegfried", ""),
	(225.,  42., city10, 1400000, "?", "?", ""),
	(390.,  43., city10, 1400000, "?", "?", ""),
	(260.,  90., city10, 1400000, "?", "?", ""),
	(380., 120., city10, 1400000, "?", "?", ""),
	(310., 180., city10, 1400000, "?", "?", ""),
	(170.,  50., city10, 1800000, "?", "?", ""),
	(295.,  28., city10, 1800000, "?", "?", ""),
	(378., 160., city10, 1800000, "?", "?", ""),

	(250., 180., city25, 2800000, "?", "?", ""),
	(363.,  40., city25, 3200000, "?", "spot", ""),
	
	(240.,  50., city05,  800000, "?", "?", ""),
	(200.,  40., city05,  800000, "?", "?", ""),
	(245.,  28., city05,  800000, "?", "?", ""),
	(284.,  20., city05,  800000, "?", "?", ""),
	(290., 100., city05,  800000, "?", "?", ""),
	(262., 140., city05,  800000, "?", "?", ""),
	(230., 160., city05,  800000, "?", "?", ""),
	(210., 180., city05,  800000, "?", "?", ""),
	(283., 178., city05,  800000, "?", "?", ""),
	(330., 110., city05,  800000, "?", "?", ""),
	(360., 110., city05,  800000, "?", "?", ""),
	(390., 150., city05,  800000, "?", "?", ""),
	(390.,  80., city05,  800000, "?", "?", ""),
	(370.,  48., city05,  800000, "?", "?", ""),
	
	(165.,  30., base00,    2000, "?", "?", ""),
	(178.,  55., base00,    2000, "?", "?", ""),
	(200.,  32., base00,    2000, "?", "?", ""),
	(222.,  50., base00,    2000, "?", "?", ""),
	(260.,  22., base00,    2000, "?", "?", ""),
	(263.,  85., base00,    2000, "?", "?", ""),
	(220., 143., base00,    2000, "?", "?", ""),
	(265., 183., base00,    2000, "?", "?", ""),
	(390., 130., base00,    2000, "?", "?", ""),
	(395.,  55., base00,    2000, "?", "?", ""),
	(320., 140., base00,    2000, "Hollow mountain", "snakehead", ""),
	(bearing_pos[0], bearing_pos[1], base00,    2000, "B", "?", ""),
]


s.add(s.image("../map_edited.png", insert=(0, 0), size=mapsize))

if grid:
	for x in range(0, mapsize[0], 10):
		s.add(s.line(start=(x, 0), end=(x, mapsize[1]), class_="grid"))

	for y in range(0, mapsize[1], 10):
		s.add(s.line(start=(0, y), end=(mapsize[0], y), class_="grid"))

matching_cities = []

for x, y, marker, size, name, code, notes in markers:
	s.add(s.use(marker, insert=(x, y)))
	text = s.text(name, insert=(x+3, y), class_="location")
	s.add(text)

	dist = math.sqrt( (position.x - x)**2 + (position.y - y)**2 )
	if config.minReach < dist < config.maxReach and marker == city10:
			matching_cities.append(name)

if len(matching_cities) != 1:
	raise Exception("There are {} matching cities: {}".format(len(matching_cities), matching_cities))

legend = (
	(city05, "500.000-1.000.000"),
	(city10, "1.000.000-2.500.000"),
	(city25, ">2.500.000"),
	)
for i, l in enumerate(legend):
	marker, text = l
	x = 90
	y = i*10 + 10
	s.add(s.use(marker, insert=(x, y)))
	s.add(s.text(text, insert=(x+3, y), class_="location"))

s.saveas("output/map.svg")

s.add(s.line(start=bearing_pos, end=bearing_pos + (position-bearing_pos)*2, stroke="black"))
s.add(s.line(start=time_pos, end=time_pos + (position-time_pos)*2, stroke="black"))

s.add(s.circle(center=position, r=3, fill="black"))

s.saveas("output/map_solution_1.svg")

s.add(s.circle(center=position, r=config.minReach, stroke="black", fill="none"))
s.add(s.circle(center=position, r=config.maxReach, stroke="black", fill="none"))

s.saveas("output/map_solution_2.svg")

s.add(s.line(start=position, end=target_pos, stroke="red"))

s.saveas("output/map_solution_3.svg")

bearing_direction = bearing_pos - position
target_direction = target_pos - position
time_direction = time_pos - position

north_angle = math.degrees(math.atan2(-1, 0))
bearing_angle = math.degrees(math.atan2(bearing_direction.y, bearing_direction.x))
time_angle = math.degrees(math.atan2(time_direction.y, time_direction.x))
target_angle = math.degrees(math.atan2(target_direction.y, target_direction.x))

with open("output/parameters.txt", "w") as f:
	f.write("""# screen coordinates
	north: {}
	bearing: {}
	time: {}
	target: {}

	# antenna coordinates
	north: {}
	bearing: {}
	time: {}
	target: {}
	""".format(
		north_angle,
		bearing_angle,
		time_angle,
		target_angle,

		convert_angle_to_antenna(north_angle),
		convert_angle_to_antenna(bearing_angle),
		convert_angle_to_antenna(time_angle),
		convert_angle_to_antenna(target_angle)
		))

with open("output/targets.tex", "w") as f:
	for x, y, marker, size, name, code, notes in markers:
		f.write("\\target{{{}}}{{{}}}{{{}}}{{{}}}{{{}}}\n".format(code, name, x, y, notes))
