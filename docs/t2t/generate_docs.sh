#!/bin/bash
txt2tags -t tex -o SANSA-Catalogue-Manual.tex 001-index.t2t
pdflatex SANSA-Catalogue-Manual.tex

txt2tags -t tex -o SANSA-Catalogue-Tests.tex tests.t2t
pdflatex SANSA-Catalogue-Tests.tex

#if you cleanup these temp files latex wont generate teh docs as it should
#rm SANSA-Catalogue-Manual.aux  SANSA-Catalogue-Manual.log   SANSA-Catalogue-Manual.out  SANSA-Catalogue-Manual.tex  SANSA-Catalogue-Manual.toc

