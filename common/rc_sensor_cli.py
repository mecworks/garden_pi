#!/usr/bin/env python

import pexpect
import os
import re

path = os.path.dirname(__file__)

class RcSensor(object):

    def __init__(self, gpio, cycles=200, discharge_delay=10):
        if gpio is None:
            raise ValueError("Must supply gpio value")
        self.gpio = gpio
        self.cycles = cycles
        self.discharge_delay = discharge_delay
        self.rcsensor_bin = os.path.join(path, '../utils/rcsensor_cli')
        self.rcsensor_cmd = 'sudo %s -g %s -c %s -d %s' % (self.rcsensor_bin, gpio, cycles, discharge_delay)
        self.rcsense_re = re.compile('(\d+)\s')

    def rc_count(self):
        """
        Returns the average of cycle number of readings from a GPIO based R/C sensor

        :return: int
        """
        m = self.rcsense_re.match(pexpect.run(self.rcsensor_cmd, timeout=150))
        count = int(m.groups()[0])
        return count



if __name__ == '__main__':
    sensor = RcSensor(22)
    print(sensor.rc_count())