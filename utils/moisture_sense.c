/*
Calculate R/C charge time of capacitive sensors on Raspberry Pi GPIOs

 */
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <stdlib.h>
#include <wiringPi.h>
#include <getopt.h>

// the event counter
volatile float cycles = 7;
volatile float discharge_time = 250;
volatile int gpio_number = 24;
unsigned int start, end;

void usage(void) {
    fprintf (stderr, "Usage: moisture_sense -c <cycles (5)> -d <capacitor discharge time in ms> -g <RPi GPIO>.\n");
}

// -------------------------------------------------------------------------
// main
int main(int argc, char *argv[]) {

    printf("Start of main()\n");;

    // Set up the wiringPi library
    if (wiringPiSetupGpio() < 0) {
        fprintf (stderr, "Unable to setup wiringPi: %s\n", strerror (errno));
        return 1;
    }

    printf("Before for options parsing\n");
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
            gpio_number = atof(optarg);
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

    printf("Before for loop\n");
    int x;
    for (x=0; x<=cycles; x++) {
        printf("In for loop\n");
        start = micros();
        pinMode(gpio_number, OUTPUT);
        //pullUpDnControl(gpio_number, PUD_OFF);
        digitalWrite(gpio_number, LOW);
        delay(discharge_time);
        pinMode(gpio_number, INPUT);
        while (digitalRead(gpio_number) != HIGH){
            delayMicroseconds(1);
        }
        end = micros();
        printf("GPIO: %s, RC Charge Time: %d\n", gpio_number, end - start);
    }
    return 0;
}