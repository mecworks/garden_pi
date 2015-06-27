all: moisture_sense rcsensor

moisture_sense: moisture_sense.c
	gcc -g -O3 -o moisture_sense moisture_sense.c -lwiringPi

rcsensor: rcsensor.c
	gcc -g -O3 -Wall -Wstrict-prototypes -fPIC -I/usr/include/python2.7 -c rcsensor.c -o rcsensor.o
	gcc -shared rcsensor.o -L/usr/local/lib -lwiringPi -o rcsensor.so
	rm rcsensor.o

clean:
	rm moisture_sense rcsensor.so rcsensor.o || true
