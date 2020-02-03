#!/bin/bash
set -e
set -x

mkdir -p output

python3 mapgen.py
python3 make_logbook.py
python3 make_testprotocols.py
python3 make_cockpit.py
python3 panel.py

(
cd code/src
make -j
)

(
cd output
pdflatex logbook.tex
pdflatex testprotocols.tex
pdflatex cockpit.tex
)
