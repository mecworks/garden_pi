all: rcsensor_cli rcsensor

rcsense_lib: rc_count.c rc_count.h
	gcc -g -O3 -c rc_count.c -Wall -Wstrict-prototypes -fPIC -I . -L/usr/local/lib -lwiringPi -o rc_count.o

rcsensor_cli: rcsensor_cli.c rcsense_lib
	gcc -g -O3 -o rcsensor_cli rcsensor_cli.c rc_count.o -I . -lwiringPi

rcsensor: rcsensor.c rcsense_lib
	gcc -g -O3 -Wall -Wstrict-prototypes -fPIC -I/usr/include/python2.7 -I . -c rcsensor.c -o rcsensor.o
	gcc -shared rcsensor.o rc_count.o -L/usr/local/lib -lwiringPi -o rcsensor.so

clean:
	rm rcsensor_cli rcsensor.so rcsensor.o rc_count.o || true

install:
	cp -v rcsensor.so ../rcsensor/
	cp -v rcsensor_cli ../utils/