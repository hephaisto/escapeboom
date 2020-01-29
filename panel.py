import svgwrite as svg


class Writer(object):
	led_radius = 2.5
	switch_radius = 3.5
	switch_height = 5.0
	push_button_radius = 5.0

	cut_stroke = "black"
	mark_stroke = "blue"
	engrave_stroke = "red"

	def __init__(self, mode, target):
		self.mode = mode
		self.s = svg.Drawing(target, width=600, height=400)
		self.s.defs.add(self.s.style(".normaltext { font-size: 8px; dominant-baseline: middle; font: monospace; }"))
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
	
	def text(self, x, y, text):
		color = {
			"doc": "black",
			"cut": self.engrave_stroke,
		}[self.mode]
		self.s.add(self.s.text(text, insert=(x, y), class_="normaltext", stroke=color))
	
	def polyline(self, points):
		color = {
			"doc": "#808080",
			"cut": self.mark_stroke,
		}[self.mode]
		self.s.add(self.s.polyline(points, stroke=color, fill="none"))

	def save(self):
		self.s.save()


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
	

for writer in (
		Writer("cut", "output/panel_cut.svg"),
		Writer("doc", "output/panel_doc.svg"),
		):
	launch_panel(writer)
	writer.save()


