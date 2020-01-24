import config

with open("templates/cockpit_description.tex", "r") as f:
	template = f.read()

with open("output/targets.tex", "r") as f:
	targets = f.read()

with open("output/cockpit.tex", "w") as f:
	f.write(template % dict(
		targets=targets,
		))
