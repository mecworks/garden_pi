all: tsl2561_test

tsl2561_test: tsl2561.o tsl2561_test.o
	gcc -Wall -O2 -o tsl2561_test tsl2561.o tsl2561_test.o

tsl2561.o: tsl2561.c
	gcc -Wall -O2 -o tsl2561.o -c tsl2561.c

tsl2561_test.o: tsl2561_test.c
	gcc -Wall -O2 -o tsl2561_test.o -c tsl2561_test.c

clean:
	rm *o || true

dist-clean: clean
	rm tsl2561_test || true