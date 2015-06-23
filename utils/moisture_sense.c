/*
Rpms calculates the fan speed in RPMs of a fan with blades
Compile as follows:

    gcc -O3 -o rpms rpms.c -lwiringPi

Run as follows:

    sudo ./rpms

    For a fan with 11 blades, sample for 200ms on WiringPi GPIO 2 (RPi GPIO R1:21/R2:27)
    
    sudo ./rpms -p 200 -b 11 -g 2

 */
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <stdlib.h>
#include <wiringPi.h>
#include <getopt.h>
#include <time.h>

// the event counter 
volatile float eventCounter = 0;
volatile float cycles = 7;
volatile float discharge_time = 250;
volatile int gpio = 24;

float rpms = 0;

// -------------------------------------------------------------------------
// myInterrupt:  called every time an event occurs
void myInterrupt(void) {
    eventCounter++;
}

void usage(void) {
    fprintf (stderr, "Usage: moisture_sense -c <cycles (5)> -d (capacitor discharge time in ms (100)> -g <RPi GPIO>.\n");
}

// -------------------------------------------------------------------------
// main
int main(int argc, char *argv[]) {

    clock_t start, end;
    double cpu_time_used;

    int option;
    while ((option = getopt (argc, argv, "c:d:g:h")) != -1) {
        switch (option) {
          case 'c':
            cycles = atof(optarg);
            break;
          case 'd':
            discharge_time = atof(optarg);
            break;
          case 'g':
            gpio = atof(optarg);
        break;
          case 'h':
            usage();
            exit(-1);
          case '?':
            usage();
            exit(-1);
          default:
            abort ();
        }
    }

    // Set up the wiringPi library
    if (wiringPiSetupGpio() < 0) {
        fprintf (stderr, "Unable to setup wiringPi: %s\n", strerror (errno));
        return 1;
        }

    for (x=0; x<=cycles; x++) {
        start = clock()
        // set up GPIO to send an interrupt on high-to-low transitions
        // and attach myInterrupt() to the interrupt
        if (wiringPiISR(gpio, INT_EDGE_FALLING, &myInterrupt) < 0) {
          fprintf (stderr, "Unable to setup ISR: %s\n", strerror (errno));
          return 1;
        }

        // Output our RPM
        eventCounter = 0;
        delay(discharge_time); // wait
        rpms = eventCounter / cycles * 60.0 * 1000/discharge_time;
        printf("%d\n", (int)rpms);

    return 0;
    }
}