/*
Calculate R/C charge time of capacitive sensors on Raspberry Pi GPIOs
Python module
 */
#include <wiringPi.h>
#include <getopt.h>
#include <Python.h>
#define DEFAULT_DISCHARGE_DELAY 10
#define DEFAULT_TIMEOUT 1000
#define DEFAULT_CYCLES 10

static PyObject* get_count(PyObject *self, PyObject *args) {

    unsigned int c,x,re[1000],med=0;
    int cycles = -1;
    int discharge_delay = -1;
    int gpio = -1;

    if (!PyArg_ParseTuple(args, "iii", &cycles, &discharge_delay, &gpio))
        return NULL;

    // Required arguments
    if (gpio == -1){
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
    return Py_BuildValue("i", med/cycles);
}

static char rcsensor_docs[] =
    "get_count(): return a value which correlates to the charge time of an RC sensor.\n";

static PyMethodDef rcsensor_funcs[] = {
    {"get_count", (PyCFunction)get_count, METH_VARARGS,
    rcsensor_docs},
    {NULL, NULL, 0, NULL}
};

void initrcsensor(void)
{
    Py_InitModule("rcsensor", rcsensor_funcs);
}