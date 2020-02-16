import math

import svgwrite as svg

style = """
.normaltext
{
	font-size: 8px;
	dominant-baseline: middle;
	font: monospace;
}
.sevensegment
{
	font-size: 12px;
	dominant-baseline: middle;
	text-anchor: middle;
}
.rightalign
{
	font-size: 8px;
	dominant-baseline: middle;
	font: monospace;
	text-anchor: end;
}
"""

padding = 15.0

class Writer(object):
	led_radius = 2.5
	switch_radius = 3.5
	switch_height = 5.0
	push_button_radius = 5.0
	turn_knob_radius = 3.0
	jack_radius = 2.5
	ps2_radius = 3.0
	textdisplay_size = (120.0, 50.0)

	cut_stroke = "black"
	mark_stroke = "blue"
	engrave_stroke = "red"

	def __init__(self, mode, target):
		self.mode = mode
		self.s = svg.Drawing(target, width=600, height=400)
		self.s.defs.add(self.s.style(style))
		self.base_x = 0.0
		self.base_y = 0.0

	def led(self, x, y, color=None):
		if self.mode != "doc":
			color = None

		fill = {
			"green": "#00FF00",
			"orange": "#FFC000",
			"red": "#FF0000",
			None: "none",
		}[color]

		self.s.add(self.s.circle(center=(x+self.base_x, y+self.base_y), r=self.led_radius, stroke=self.cut_stroke, fill=fill))
	
	def switch2(self, x, y):
		fill = {
			"doc": "white",
			"cut": "none",
		}[self.mode]
		self.s.add(self.s.circle(center=(x+self.base_x, y+self.base_y), r=self.switch_radius, stroke=self.cut_stroke, fill=fill))
		if self.mode == "doc":
			self.s.add(self.s.ellipse(center=(x+self.base_x, y+self.base_y-self.switch_height), r=(self.switch_radius, self.switch_height), stroke="none", fill="grey"))
	
	def push_button(self, x, y, color):
		fill = {
			"green": "#008000",
			"red": "#800000",
		}[color]
		if self.mode != "doc":
			fill = "none"

		self.s.add(self.s.circle(center=(x+self.base_x, y+self.base_y), r=self.push_button_radius, stroke=self.cut_stroke, fill=fill))
	
	def ps2(self, x, y):
		self.s.add(self.s.circle(center=(x+self.base_x, y+self.base_y), r=self.ps2_radius, stroke=self.cut_stroke, fill="none"))
	
	def textdisplay(self, x, y):
		size = self.textdisplay_size
		self.s.add(self.s.rect(insert=(x-size[0]/2, y-size[1]/2), size=size, stroke=self.cut_stroke, fill="none"))
	
	def text(self, x, y, text, align=""):
		color = {
			"doc": "black",
			"cut": self.engrave_stroke,
		}[self.mode]
		class_ = {
			"": "normaltext",
			"left": "normaltext",
			"right": "rightalign",
		}[align]
		self.s.add(self.s.text(text, insert=(x, y), class_=class_, stroke=color))
	
	def polyline(self, points):
		color = {
			"doc": "#808080",
			"cut": self.mark_stroke,
		}[self.mode]
		self.s.add(self.s.polyline(points, stroke=color, fill="none"))

	def save(self):
		self.s.save()
	
	def seven_segment(self, x, y, color):
		stroke = {
			"doc": "black",
			"cut": self.cut_stroke,
		}[self.mode]

		width = 60.0 # TODO
		height = 20.0 # TODO

		self.s.add(self.s.rect(insert=(x-width/2, y-height/2), size=(width, height), stroke=stroke, fill="none"))
		if self.mode == "doc":
			self.s.add(self.s.text("12:34", insert=(x, y), class_="sevensegment", stroke=color))
	
	def turn_knob(self, x, y):
		self.s.add(self.s.circle(center=(x, y), r=self.turn_knob_radius, stroke=self.cut_stroke))

		if self.mode == "doc":
			self.s.add(self.s.circle(center=(x, y), r=self.turn_knob_radius+5.0, fill="gray", stroke="black"))
	
	def turn_knob_labels(self, x, y, labels):
		radius = 20.0
		for angle, label in labels:
			end_x = x + math.cos(angle)*radius
			end_y = y+math.sin(angle)*radius
			self.polyline([(x, y), (end_x, end_y)])
			self.text(end_x, end_y, label, align="right" if end_x<x else "left")
	
	def jack(self, x, y):
		self.s.add(self.s.circle(center=(x, y), r=self.jack_radius, stroke=self.cut_stroke, fill="none"))
	
	def with_label(self, func, x, y, label, *args, **kwargs):
		func(x, y, *args, **kwargs)
		self.polyline([(x, y), (x+padding, y)])
		self.text(x+padding, y, label)


def launch_panel(writer):
	width = 15.0
	left = 20.0
	x_text = 110.0

	y_switch = 10.0
	y_power = 30.0
	y_programmed = 50.0
	y_program = 70.0

	writer.polyline([(left, y_switch), (x_text, y_switch), (x_text, y_power), (left, y_power)])
	writer.text(x_text, (y_switch+y_power)/2, "POWER")

	writer.polyline([(left, y_programmed), (x_text, y_programmed)])
	writer.text(x_text, y_programmed, "READY")

	writer.polyline([(left, y_program), (x_text, y_program)])
	writer.text(x_text, y_program, "PROGRAM")

	for i in range(6):
		x = left + width * i
		writer.switch2(x, y_switch)
		writer.led(x, y_power, "green")
		writer.led(x, y_programmed, "orange")
		writer.push_button(x, y_program, "green")
	
	x_launch = 170.0
	writer.with_label(writer.push_button, x_launch, y_switch, "LAUNCH 1", "red")
	writer.with_label(writer.push_button, x_launch, y_program, "LAUNCH 2", "red")


def antenna_panel(writer):
	left_center = 15.0

	right_center = 130.0

	top = 15.0
	bottom = 30.0

	writer.with_label(writer.led, left_center, top, "TURNING", "green")
	writer.with_label(writer.led, left_center, bottom, "MALFUNCTION", "red")

	writer.with_label(writer.push_button, right_center, top, "LEFT", "green")
	writer.with_label(writer.push_button, right_center, bottom, "RIGHT", "green")

def sender_panel(writer):
	writer.seven_segment(60.0, 30.0, "green")
	writer.turn_knob(120.0, 30.0)
	
	source_x = 80.0
	source_y = 80.0

	labels = [(i*0.6, label) for i, label in enumerate((
		"off",
		"morse",
		"crypt",
		"aux",
		"plain",
		"microphone",
		"board com1",
		"board com2",
		))]
	writer.turn_knob_labels(source_x, source_y, labels)
	writer.turn_knob(source_x, source_y)

	writer.with_label(writer.push_button, 120.0, 120.0, "MORSE", "green")
	writer.with_label(writer.jack, 60.0, 120.0, "AUX IN")

def clock_panel(writer):
	writer.seven_segment(60.0, 30.0, "red")
	writer.with_label(writer.led, 40.0, 50.0, "SYNC", "green")

def lock_panel(writer):
	for i in range(3):
		y = (3-i) * 20.0 + 10
		lvl = i+1
		writer.with_label(writer.led, 40.0, y, "LVL{} LOCK".format(lvl), "red")
		writer.push_button(20.0, y, "red")
	writer.with_label(writer.push_button, 40.0, 90.0, "UNLOCK", "green")
	writer.with_label(writer.led, 40.0, 110.0, "INPUT LOCK", "red")

def selfdestruct_panel(writer):
	writer.seven_segment(60.0, 30.0, "red")
	writer.with_label(writer.push_button, 40.0, 60.0, "START", "red")
	writer.with_label(writer.push_button, 40.0, 80.0, "ABORT", "red")

def encryption_panel(writer):
	writer.with_label(writer.switch2, 60, 30, "POWER")
	writer.led(30, 30, "green")
	writer.with_label(writer.switch2, 60, 50, "MODE")
	writer.with_label(writer.push_button, 60, 70, "RESET", "red")

def entry_panel(writer):
	writer.textdisplay(90, 30)
	writer.ps2(90, 70)

for out_type in ("cut", "doc"):
	for out_name, out_function in (
		("launch", launch_panel),
		("antenna", antenna_panel),
		("sender", sender_panel),
		("clock", clock_panel),
		("lock", lock_panel),
		("selfdestruct", selfdestruct_panel),
		("encryption", encryption_panel),
		("entry", entry_panel),
		):
		writer = Writer(out_type, "output/{}_{}.svg".format(out_name, out_type))
		out_function(writer)
		writer.save()

