#!/usr/bin/env python

import time
import sys
import signal
from rcsensor import rcsensor

# Sensor GPIOs:
# PIN    GPIO
# 13     21/27
# 15     22
# 16     23
# 18     24
#
# relays:
# 5      3
# 8      14
# 10     15
# 11     17

log_file = open("SensorData.txt", "w")

def signal_handler(signal, frame):
    """
    Handle Ctrl-C

    :param signal:
    :param frame:
    :return:
    """
    print '\nCtrl-C detected, cleaning up...'
    cleanup(force_exit=True)


def cleanup(force_exit=False):
    log_file.close()
    if force_exit is True:
        sys.exit(0)


def timestamp():
    """
    Return our standard timestamp, the unix epic seconds, accurate to 4 decimal places.

    :return: str
    """
    return '{0:.4f}'.format(time.time())


def rc_analog(gpio, cycles=200, discharge_delay=10):
    return rcsensor.get_rc_counts(gpio, cycles, discharge_delay)


def usage():
    print('Usage: soil_sensor.py <gpio> [<cycles=10>]')
    sys.exit(0)


def main(argv):
    try:
        gpio = int(argv[1])
    except:
        usage()

    try:
        cycles = int(argv[2])
    except ValueError:
        usage()
    except IndexError:
        cycles = 10

    while True:
        reading = rc_analog(gpio, cycles)
        msg = timestamp() + ", " + "GPIO: %s, Cycles: %s, %s" % (gpio, cycles, str(reading))
        print msg
        log_file.write(msg + '\n')


signal.signal(signal.SIGINT, signal_handler)
main(sys.argv)
cleanup()

