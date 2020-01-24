#!/usr/bin/python3

import random
from encrypt import encrypt, format_to_hex
import config

random.seed(1337)

template = r"""
	\clearpage
	\section*{Test protocol}
	\subsection*{Identifying information}
	\begin{longtable}{|p{8cm}|p{3cm}|}\hline
		\field{Device variant}{\planeType}
		\field{Device serial number}{%(device_serial)d}
		\field{Propelling unit serial number}{%(propeller_serial)d}
		\field{Communication unit serial number}{%(comm_serial)d}
		\field{Payload release unit serial number}{%(payload_serial)d}
		\field{Main control unit serial number}{%(main_serial)d}
		\field{Overall test result}{PASS}
	\end{longtable}

	\subsection*{Detailed test results}
	\begin{longtable}{|p{6.2cm}|p{3cm}|p{2cm}|p{1.3cm}|}\hline
		Test & Expectation & Actual & Result \\\hline\endfirsthead
		\test{Propellant leakage tank 1}{$<20\mu l/h$}{$%(leakage1)d\mu l/h$}
		\test{Propellant leakage tank 2}{$<20\mu l/h$}{$%(leakage2)d\mu l/h$}
		\test{Carrier frequency}{$|f-%(carrier_frequency)d|<1kHz$}{%(carrier_frequency)d}
		\test{Communication output amplitude}{$\geq 17$}{$%(comm_amplitude)d$}
		\test{Communication test %(comm_input)s}{%(comm_output)s}{%(comm_output)s}
		\test{Communication cutoff angle left}{$8^\circ \leq \phi \leq 10^\circ$}{$%(cutoff_left)d^\circ$}
		\test{Communication cutoff angle right}{$8^\circ \leq \phi \leq 10^\circ$}{$%(cutoff_right)d^\circ$}
		\test{Communication cutoff angle top}{$8^\circ \leq \phi \leq 10^\circ$}{$%(cutoff_top)d^\circ$}
		\test{Communication cutoff angle bottom}{$8^\circ \leq \phi \leq 10^\circ$}{$%(cutoff_bottom)d^\circ$}
		\test{Payload release 200kg}{released}{released}
		\test{Payload release 2000kg}{%(heavy_payload)s}{%(heavy_payload)s}
		\test{Pitch sensor readout $10^\circ$}{$9.5^\circ \leq \alpha \leq 10.5^\circ$}{$%(pitch_10).1f^\circ$}
		\test{Pitch sensor readout $30^\circ$}{$29.5^\circ \leq \alpha \leq 30.5^\circ$}{$%(pitch_30).1f^\circ$}
		\test{Roll sensor readout $10^\circ$}{$9.5^\circ \leq \beta \leq 10.5^\circ$}{$%(roll_10).1f^\circ$}
		\test{Roll sensor readout $30^\circ$}{$29.5^\circ \leq \beta \leq 30.5^\circ$}{$%(roll_30).1f^\circ$}
		\test{Yaw integrator drift}{$|\gamma| < 0.1^\circ/h$}{$%(yaw_drift).2f^\circ$}
		\test{Yaw integrator full rotation}{$|\gamma| < 0.1^\circ$}{$%(yaw_rotation).2f^\circ$}
		\test{Speed readout at cruise speed}{$%(speed_min).1f \leq v \leq %(speed_max).1f$}{$%(speed).1f$}
	\end{longtable}


"""

semirandom_data = []

available_keys = [i for i in range(1, 256) if i != config.correct_key]
random.shuffle(available_keys)

semirandom_data.append(dict(
	key=config.correct_key,
	big_payload=True,
	heavy_payload=True,
	expended=False,
	carrier_frequency=config.carrier_frequency
	))

def add(N, heavy, expended):
	for i in range(N):
		semirandom_data.append(dict(
		key = available_keys.pop(),
		heavy_payload = heavy,
		expended = expended,
		carrier_frequency = random.randrange(101, 999),
		))

#   N  heavy  expended
add(5, True , False)
add(4, True , True)
add(5, False, False)
add(5, False, True)

speed = round(config.minReach/config.hours_to_impact, 1)

text_items = ""

for i, data in enumerate(semirandom_data):
	key = random.randrange(0, 256)
	text_items += template % dict(
		device_serial = random.randrange(10000, 100000),
		propeller_serial = random.randrange(10000, 100000),
		comm_serial = random.randrange(10000, 100000),
		payload_serial = random.randrange(10000, 100000),
		main_serial = random.randrange(10000, 100000),
		leakage1 = random.randrange(2, 19),
		leakage2 = random.randrange(2, 19),
		comm_input = format_to_hex(encrypt(key, "test\n")),
		comm_output = format_to_hex(encrypt(key, "ok\n")),
		comm_amplitude = random.randrange(17, 20),
		cutoff_left = random.randrange(8, 11),
		cutoff_right = random.randrange(8, 11),
		cutoff_top = random.randrange(8, 11),
		cutoff_bottom = random.randrange(8, 11),
		pitch_10 = random.uniform(9.5, 10.5),
		pitch_30 = random.uniform(29.5, 30.5),
		roll_10 = random.uniform(9.5, 10.5),
		roll_30 = random.uniform(29.5, 30.5),
		yaw_drift = random.uniform(-0.09, 0.09),
		yaw_rotation = random.uniform(-0.09, 0.09),
		speed_min = speed-1,
		speed = speed + random.uniform(-1, 1),
		speed_max = speed+1,
		heavy_payload = "released" if data["heavy_payload"] else "N/A",
		carrier_frequency = data["carrier_frequency"],
		)

with open("templates/testprotocols.tex", "r") as f:
	document_template = f.read()

output = document_template % dict(protocols=text_items)


with open("output/testprotocols.tex", "w") as f:
	f.write(output)
