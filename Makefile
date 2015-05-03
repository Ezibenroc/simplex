# HELLO, I AM A STUPID AND USELESS MAKEFILE

toto:
	@echo ./main.py $$\* > toto
	@chmod +x toto

opt: toto
	@cp -f toto totoopt

clean:
	@rm -f toto totoopt
