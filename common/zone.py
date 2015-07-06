#!/usr/bin/env python

from common.relay import Relay
from common.temp_sensor import TempSensor
from common.rc_sensor import RcSensor
from common.temp_sensor import TempSensor
import ConfigParser
import time
import os

# Config file
path = os.path.dirname(__file__)
config_file = os.path.join(path, '../garden_pi.cfg')
conf_parser = ConfigParser.ConfigParser()
conf_parser.read(config_file)
DEBUG = conf_parser.getboolean('main', 'debug')

class Zone (object):

    def __init__(self, name=None, alias=None, moisture_sensor_gpio=None, relay_gpio=None, moisture_water_threshold=None, watering_duration=None, min_seconds_between_waterings=18000, temp_sensor_id=None):
        self.name = name
        self.alias = alias
        if moisture_sensor_gpio in [None, 'None']:
            self.moisture_sensor = None
        else:
            self._moisture_sensor_gpio = moisture_sensor_gpio
            self.moisture_sensor = RcSensor(self._moisture_sensor_gpio)
        self._relay_gpio = relay_gpio
        self.relay = Relay(self._relay_gpio)
        self.moisture_water_threshold = moisture_water_threshold
        self.watering_duration = watering_duration
        self.min_seconds_between_waterings = min_seconds_between_waterings
        if temp_sensor_id in [None, 'None']:
            self.temp_sensor = None
        else:
            self._temp_sensor_id = temp_sensor_id
            self.temp_sensor = TempSensor(self._temp_sensor_id)
        self.last_water_time = None

    def water(self):
        """
        Waters a zone
        Returns True if able to water, returns False if unable (last water time is too recent)

        :return: bool
        """
        now = time.time()
        if self.last_water_time is None:
            self.last_water_time = now
        if (now == self.last_water_time) or (now - self.last_water_time > self.min_seconds_between_waterings):
            self.last_water_time = now
            if DEBUG:
                print("Debug mode, not turning on relay")
            else:
                self.relay.set_state(self.relay.ON)
            time.sleep(self.watering_duration)
            self.relay.set_state(self.relay.OFF)
            return True
        else:
            print('Not enought time has elapsed since last watering. Not starting watering cycle.')
            return False

    def water_now(self):
        self.last_water_time = time.time()
        self.relay.set_state(self.relay.ON)
        time.sleep(self.watering_duration)
        self.relay.set_state(self.relay.OFF)

    @property
    def temp(self):
        if self.temp_sensor is None:
            return None
        else:
            return self.temp_sensor.temp_f

    @property
    def moisture(self):
        if self.moisture_sensor is None:
            return None
        else:
            return self.moisture_sensor.rc_count()
