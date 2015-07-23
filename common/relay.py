#!/usr/bin/env python

# A Raspberry Pi GPIO based relay device
import RPi.GPIO as GPIO
from common.adafruit.Adafruit_MCP230xx.Adafruit_MCP230xx import Adafruit_MCP230XX

class Relay(object):

    def __init__(self, mcp_pin):
        """
        Initialize a relay

        :param mcp_pin: BCM gpio number that is connected to a relay
        :return:
        """
        self.ON = 0
        self.OFF = 1
        self._i2c_address = 0x27
        self._mcp_pin = mcp_pin
        if GPIO.RPI_REVISION == 1:
            i2c_busnum = 0
        else:
            i2c_busnum = 1
        self._relay = Adafruit_MCP230XX(busnum=i2c_busnum, address=self._i2c_address, num_gpios = 16)
        self._relay.output(self._mcp_pin, self.OFF)
        self._relay.config(self._mcp_pin, self._relay.OUTPUT)
        self._relay.output(self._mcp_pin, self.OFF)
        self.state = self.OFF

    def set_state(self, state):
        """
        Set the state of the relay.  relay.ON, relay.OFF

        :param state:
        :return:
        """
        if state == self.ON:
            self._relay.output(self._mcp_pin, self.ON)
            state = self.ON
        elif state == self.OFF:
            self._relay.output(self._mcp_pin, self.OFF)
            state = self.OFF

    def toggle(self):
        """
        Toggle the state of a relay
        :return:
        """
        if self.state == self.ON:
            self._relay.output(self._mcp_pin, self.OFF)
            self.state = self.OFF
        else:
            self._relay.output(self._mcp_pin, self.ON)
            self.state = self.ON

    def get_state(self):
        return self.state


if __name__ == '__main__':

    import time

    pause = .15
    for pin in range(16):
        print("Pin: %s" % pin)
        r = Relay(pin)
        r.set_state(r.ON)
        time.sleep(pause)
        r.set_state(r.OFF)
        time.sleep(pause)
        r.toggle()
        time.sleep(pause)
        r.toggle()
        time.sleep(pause)