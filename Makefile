# HELLO, I AM A STUPID AND USELESS MAKEFILE

toto:
	@echo pypy -OO -m main $$\* > toto
	@chmod +x toto

opt:toto
	cp -f toto totoopt
