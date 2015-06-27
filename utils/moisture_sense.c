/*
Calculate R/C charge time of capacitive sensors on Raspberry Pi GPIOs

 */
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <stdlib.h>
#include <wiringPi.h>
#include <getopt.h>
#define DEFAULT_DISCHARGE_DELAY 10
#define DEFAULT_TIMEOUT 1000
#define DEFAULT_CYCLES 10

void usage(void) {
    fprintf (stderr, "Usage: moisture_sense -g <RPi GPIO> -c [cycles (ms): 1000] -d [capacitor discharge time (ms): 10] -t [timeout (ms): 1000].\n");
}

// main
int main(int argc, char *argv[]) {

    unsigned int c,x,re[1000],med=0;
    int cycles = -1;
    int discharge_delay = -1;
    int gpio = -1;

    int option;
    while ((option = getopt (argc, argv, "c:d:g:h")) != -1) {
        switch (option) {
          case 'c':
            cycles = atof(optarg);
            if (cycles>1000) {
                fprintf(stderr, "Cycles must be less than 1000.\n");
                usage();
                exit(-1);
            }
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

    wiringPiSetup();
    int pin;
    for (pin = 0 ; pin < 16 ; ++pin) {
        pinMode (pin, OUTPUT) ;
        digitalWrite (pin, LOW) ;
    }

    if (wiringPiSetupGpio()<0)
        exit (1) ;

    for (x=0;x<cycles;x++) {
        c=0;;
        pinMode (gpio, OUTPUT);;
        digitalWrite (gpio, LOW);
        delay(discharge_delay);
        pinMode (gpio, INPUT);
        while (digitalRead(gpio)==LOW) {
            c++;
        }
        re[x]=c;
    }
    med=0;
    for (x=0;x<cycles;x++)
        med+=re[x];
    printf("%d\n",med/cycles);
    return 0;
}