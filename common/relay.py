#!/usr/bin/env python

# A Raspberry Pi GPIO based relay device
import RPi.GPIO as GPIO
from common.adafruit.Adafruit_MCP230xx.Adafruit_MCP230xx import Adafruit_MCP230XX

class Relay(object):

    _mcp23017_chip = {}  # Conceivably, we could have up to 8 of these as there are a possibility of 8 MCP chips on a bus.

    def __init__(self, mcp_pin, i2c_address=0x27):
        """
        Initialize a relay

        :param mcp_pin: BCM gpio number that is connected to a relay
        :return:
        """
        self.ON = 0
        self.OFF = 1
        self._i2c_address = i2c_address
        self._mcp_pin = mcp_pin
        if GPIO.RPI_REVISION == 1:
            i2c_busnum = 0
        else:
            i2c_busnum = 1
        if not self._mcp23017_chip.has_key(self._i2c_address):
            self._mcp23017_chip[self._i2c_address] = Adafruit_MCP230XX(busnum=i2c_busnum, address=self._i2c_address, num_gpios=16)
        self._relay = self._mcp23017_chip[self._i2c_address]
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
            self.state = self.ON
        elif state == self.OFF:
            self._relay.output(self._mcp_pin, self.OFF)
            self.state = self.OFF

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

    r1 = Relay(10)
    r2 = Relay(2)
    r3 = Relay(15)

    r1.set_state(r1.ON)
    print(r1._mcp_pin)
    r2.set_state(r2.ON)
    print(r2._mcp_pin)
    r3.set_state(r3.ON)
    print(r3._mcp_pin)
    time.sleep(1)
    r1.set_state(r1.OFF)
    r2.set_state(r2.OFF)
    r3.set_state(r3.OFF)