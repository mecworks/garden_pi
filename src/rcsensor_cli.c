/*
Calculate R/C charge time of capacitive sensors on Raspberry Pi GPIOs

 */
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <stdlib.h>
#include <getopt.h>
#include "rc_count.h"
#define DEFAULT_DISCHARGE_DELAY 10
#define DEFAULT_TIMEOUT 1000
#define DEFAULT_CYCLES 10

void usage(void) {
    fprintf (stderr, "Usage: moisture_sense -g <RPi GPIO> -c [cycles (ms): 1000] -d [capacitor discharge time (ms): 10].\n");
}

// main
int main(int argc, char *argv[]) {

    unsigned int c,x,med=0,val;
    int cycles = -1;
    int discharge_delay = -1;
    int gpio = -1;

    int option;
    while ((option = getopt (argc, argv, "c:d:g:h")) != -1) {
        switch (option) {
          case 'c':
            cycles = atof(optarg);
            break;
          case 'd':
            discharge_delay = atof(optarg);
            break;
          case 'g':
            gpio = atof(optarg);
            break;
          case 'h':
            usage();
            exit(0);
          case '?':
            usage();
            exit(0);
          default:
            abort();
        }
    }

    // Required arguments
    if (gpio == -1){
        usage();
        exit(-1);
    }
    // default values
    if (discharge_delay == -1)
        discharge_delay = DEFAULT_DISCHARGE_DELAY;
    if (cycles == -1)
        cycles = DEFAULT_CYCLES;
    unsigned int re[cycles];

    val = get_count(gpio, cycles, discharge_delay);
    printf("%d\n",val);
    return 0;
}