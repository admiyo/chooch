
all: garzone.pdf garzone.midi
	evince garzone.ps

garzone.midi:  garzone.abc
	abc2midi garzone.abc

garzone.pdf: garzone.abc
	abcm2ps -O - garzone.abc | ps2pdf - garzone.pdf

garzone.abc: chooch.py
	./chooch.py

clean:
	rm -r garzone*
