
all: garzone.ps garzone.midi
	evince garzone.ps

garzone.midi:  garzone.abc
	abc2midi garzone.abc

garzone.ps: garzone.abc
	yaps garzone.abc


garzone.abc: chooch.py
	./chooch.py

clean:
	rm -r garzone*
