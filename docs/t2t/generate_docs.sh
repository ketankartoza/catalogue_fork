#!/bin/bash
txt2tags -t tex -o SANSA-Catalogue-Manual.tex 001-index.t2t
pdflatex SANSA-Catalogue-Manual.tex
rm SANSA-Catalogue-Manual.aux  SANSA-Catalogue-Manual.log   SANSA-Catalogue-Manual.out  SANSA-Catalogue-Manual.tex  SANSA-Catalogue-Manual.toc

