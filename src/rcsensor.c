/*
Calculate R/C charge time of capacitive sensors on Raspberry Pi GPIOs
Python module
 */
#include <getopt.h>
#include <Python.h>
#include "rc_count.h"
#define DEFAULT_DISCHARGE_DELAY 10
#define DEFAULT_TIMEOUT 1000
#define DEFAULT_CYCLES 10

static PyObject* get_rc_counts(PyObject *self, PyObject *args) {

    unsigned int ret;
    int gpio = -1;
    int cycles = -1;
    int discharge_delay = -1;

    if (!PyArg_ParseTuple(args, "iii", &gpio, &cycles, &discharge_delay))
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

    ret = get_count(gpio, cycles, discharge_delay);
    return Py_BuildValue("i", ret);
}

static char rcsensor_docs[] =
    "get_rc_counts(): return a value which correlates to the charge time of an RC sensor.\n";

static PyMethodDef rcsensor_funcs[] = {
    {"get_rc_counts", (PyCFunction)get_rc_counts, METH_VARARGS,
    rcsensor_docs},
    {NULL, NULL, 0, NULL}
};

void initrcsensor(void)
{
    Py_InitModule("rcsensor", rcsensor_funcs);
}