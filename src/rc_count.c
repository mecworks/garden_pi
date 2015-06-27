#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <stdlib.h>
#include <wiringPi.h>
#include "rc_count.h"

int get_count(int gpio, int cycles, int discharge_delay) {
    unsigned int c,x,re[cycles],med=0;

    if (wiringPiSetupGpio()<0)
        exit (1) ;
    pullUpDnControl (gpio, PUD_OFF);
    for (x=0;x<cycles;x++) {
        c=0;
        pinMode (gpio, OUTPUT);
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
    return med/cycles;
}