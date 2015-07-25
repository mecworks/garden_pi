Code from here:

  http://dino.ciuffetti.info/2014/03/tsl2561-light-sensor-on-raspberry-pi-in-c/

Build:

  gcc -Wall -O2 -o TSL2561.o -c TSL2561.c
  gcc -Wall -O2 -o TSL2561_test.o -c TSL2561_test.c
  gcc -Wall -O2 -o TSL2561_test TSL2561.o TSL2561_test.o

Make sure the following moduled are loaded:

  modprobe i2c_bcm2708
  modprobe i2c_dev

