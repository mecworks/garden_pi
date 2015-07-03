#!/usr/bin/env python

# A Raspberry Pi GPIO based relay device

import RPi.GPIO as GPIO

class Relay(object):

    def __init__(self, gpio_pin):
        """
        Initialize a relay

        :param gpio_pin: BCM gpio number that is connected to a relay
        :return:
        """
        self.ON = 0
        self.OFF = 1
        self.gpio_pin = gpio_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.OUT)
        GPIO.output(gpio_pin, self.OFF)
        self.state = self.OFF

    def set_state(self, state):
        """
        Set the state of the relay.  relay.ON, relay.OFF, True, False

        :param state:
        :return:
        """
        if state is True:
            state = self.ON
        elif state is False:
            state = self.OFF
        else:
            GPIO.output(self.gpio_pin, state)
        self.state = state

    def toggle(self):
        """
        Toggle the state of a relay
        :return:
        """
        if self.state == self.ON:
            GPIO.output(self.gpio_pin, self.OFF)
            self.state = self.OFF
        else:
            GPIO.output(self.gpio_pin, self.ON)
            self.state = self.ON

if __name__ == '__main__':

    import sys
    import time
    
    GPIO.setwarnings(False)
    def usage(prog):
        print('Usage: %s <gpio>' % prog)
        sys.exit(0)

    def main(argv):
        try:
            gpio = int(argv[1])
        except:
            usage(argv[0])
        r = Relay(gpio)
        r.set_state(r.ON)
        time.sleep(10)
        r.set_state(r.OFF)
        GPIO.cleanup()

    main(sys.argv)
