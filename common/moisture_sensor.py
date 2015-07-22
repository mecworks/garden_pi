#!/usr/bin/env python

from common.adafruit.Adafruit_ADS1x15 import Adafruit_ADS1x15
# from threading import RLock    #  May be needed if we end up multiplexing readings with a 16:1 analog mux

class VH400MoistureSensor(object):
    """
    This class supports the Vegetronix VH400 MoistureSensor
    VH400 Piecewise Curve

        Most curves can be approximated with linear segments of the form:

        y= m*x-b,

        where m is the slope of the line

        The VH400's Voltage to VWC curve can be approximated with 4 segments of the form:

        VWC= m*V-b

        where  V is voltage.

        m= (VWC2 - VWC1)/(V2-V1)

        where V1 and V2 are voltages recorded at the respective VWC levels of VWC1 and VWC2.
        After m is determined, the y-axis intercept coefficient b can be found by inserting one of the end points into the equation:

        b= m*v-VWC

        Voltage Range	Equation
        0 to 1.1V	VWC= 10*V-1
        1.1V to 1.3V	VWC= 25*V- 17.5
        1.3V  to 1.82V	VWC= 48.08*V- 47.5
        1.82V to 2.2V	VWC= 26.32*V- 7.89

    Some notes from https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code/blob/master/Adafruit_ADS1x15/ads1x15_ex_singleended.py

    Select the gain
      gain = 6144  # +/- 6.144V
      gain = 4096  # +/- 4.096V
      gain = 2048  # +/- 2.048V
      gain = 1024  # +/- 1.024V
      gain = 512   # +/- 0.512V
      gain = 256   # +/- 0.256V

    Select the sample rate
      sps = 8    # 8 samples per second
      sps = 16   # 16 samples per second
      sps = 32   # 32 samples per second
      sps = 64   # 64 samples per second
      sps = 128  # 128 samples per second
      sps = 250  # 250 samples per second
      sps = 475  # 475 samples per second
      sps = 860  # 860 samples per second

    Possible ADS1x15 i2c address: 0x48, 0x48, 0x4a, 0x4b
    Our default is 0x49  This will probably be hard-coded on the board.

    ADS1015 = 0x00  # 12-bit ADC
    ADS1115 = 0x01	# 16-bit ADC
    """
    ADS1115 = 0x01

    def __init__(self, i2c_addr=49, ADS1x15_pin=None, ADS1x15_gain=4096, ADS1x15_sps=256, average_readings=1):
        """
        A Vegetronix VH400 MoistureSensor.

        :param i2c_addr: i2c address of the ADS1115 chip
        :type i2c_addr: hex
        :param ADS1x15_pin: Which ADC do we read when talking to this sensor?
        :type ADS1x15_pin: int
        :param ADS1x15_gain: Input gain.  This shouldn't be changed from 4096 as the VH400 has a 0-3v output
        :type ADS1x15_gain: int
        :param ADS1x15_sps: How many samples per second will the ADC take?  Lower = less noise, Higher = faster readings.
        :type ADS1x15_sps: int
        :param average_readings: How many readings to we average before returning a value
        :type average_readings: int
        """
        self.i2c_addr = i2c_addr
        self.pin = ADS1x15_pin
        self.gain = ADS1x15_gain
        self.sps = ADS1x15_sps
        self.adc = Adafruit_ADS1x15.ADS1x15(address=self.i2c_addr, ic=self.ADS1115)
        self.average_readings = average_readings

    def read_percent(self):
        """
        Return the Volumetric Water Content (VWC) % of the soil

        :return: float
        """
        v = self.read_raw_voltage()
        if 0.0 <= v <= 1.1:
            return 10 * v -1
        elif 1.1 < v <= 1.3:
            return 25 * v - 17.5
        elif 1.3 < v <= 1.82:
            return 48.08 * v - 47.5
        elif 1.82 < v:
            return 26.32* v - 7.89

    def read_raw_voltage(self):
        """
        Return the raw sensor voltage.  Average readings before returning the value

        :return: float
        """
        reading = 0.0
        for _i in range(self.average_readings):
            reading += self.adc.readADCSingleEnded(self.pin, self.gain, self.sps)
        return reading / self.average_readings / 1000.0

