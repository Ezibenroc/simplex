# HELLO, I AM A STUPID AND USELESS MAKEFILE

toto:
	@echo ./main.py $$\* > toto
	@chmod +x toto

opt: toto
	@cp -f toto totoopt

print:
	@echo ./main.py -l /tmp/simplex.tex $$\* > totoprint
	@echo pdflatex -output-directory /tmp -interaction=batchmode /tmp/simplex.tex \>/dev/null >> totoprint
	@echo cp /tmp/simplex.pdf . >> totoprint
	@echo echo "Produced file simplex.pdf" >> totoprint
	@chmod +x totoprint

clean:
	@rm -f toto totoopt totoprint
