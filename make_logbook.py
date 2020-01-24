import config

with open("templates/logbook.tex", "r") as f:
	template = f.read()

with open("output/logbook.tex", "w") as f:
	f.write(template % dict(
		vehicle1="TODO",
		vehicle2="TODO",
		vehicle3="TODO",
		vehicle4="TODO",
		shipname="TODO",
		))
