#!/usr/bin/env python

from common.rcsensor import rcsensor

class Zone (object):

    def __init__(self, moisture_sensor_gpio, relay_gpio, moisture_water_threshold, watering_duration, min_wait_between_cycles, temp_sensor):
        self.moisture_sensor_gpio = moisture_sensor_gpio
        self.relay_gpio = relay_gpio
        self.moisture_water_threshold = moisture_water_threshold
        self.watering_duration = watering_duration
        self.min_wait_between_cycles = min_wait_between_cycles
        self.temp_sensor = temp_sensor
