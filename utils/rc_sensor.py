#!/usr/bin/env python

from common.rcsensor import rcsensor as rcsensor


class RcSensor(object):

    def __init__(self, gpio, cycles=200, discharge_delay=10):
        if gpio is None:
            raise ValueError("Must supply gpio value")
        self.gpio = gpio
        self.cycles = cycles
        self.discharge_delay = discharge_delay

    def rc_count(self):
        """
        Returns the average of cycle number of readings from a GPIO based R/C sensor

        :return: int
        """
        return rcsensor.get_rc_counts(self.gpio, self.cycles, self.discharge_delay)
