/*
Calculate R/C charge time of capacitive sensors on Raspberry Pi GPIOs

 */
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <stdlib.h>
#include <wiringPi.h>
#include <getopt.h>

void usage(void) {
    fprintf (stderr, "Usage: moisture_sense -c <cycles (<1000)> -d <capacitor discharge time in ms> -g <RPi GPIO>.\n");
}

// main
int main(int argc, char *argv[]) {

    int c,x,re[1000],med=0;
    int cycles;
    int discharge_delay;
    int gpio;

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
            exit(-1);
          case '?':
            usage();
            exit(-1);
          default:
            usage();
            exit(0);
        }
    }

    if (wiringPiSetupGpio()<0)
        exit (1) ;

    for (x=0;x<cycles;x++) {
        c=0;
        pinMode (gpio, OUTPUT);
        digitalWrite (gpio, LOW);
        delay(discharge_delay);
        pinMode (gpio, INPUT);
        while (digitalRead(gpio)==LOW)
            c++;
        re[x]=c;
    }
    med=0;
    for (x=0;x<cycles;x++)
        med+=re[x];
    printf("%d\n",med/cycles);
    return 0;
}