#!/usr/bin/env python

from common.relay import Relay
from common.moisture_sensor import VH400MoistureSensor
from common.temp_sensor import TempSensor
import ConfigParser
import time
import os
import cPickle as Pickle

# Config file
path = os.path.dirname(__file__)
config_file = os.path.join(path, '../garden_pi.cfg')
conf_parser = ConfigParser.ConfigParser()
conf_parser.read(config_file)
DEBUG = conf_parser.getboolean('main', 'debug')


class Zone (object):
    """
    A Zone handles all the attributes and functions of a zone, sensing, watering, timings, etc.
    """

    def __init__(self, name=None, alias=None, moisture_sensor_pin=None, mcp_pin=None, moisture_water_threshold=None, watering_duration=None, min_seconds_between_waterings=18000, temp_sensor_id=None, temp_scale='f'):
        self.name = name
        self.alias = alias
        if moisture_sensor_pin in [None, 'None']:
            self.moisture_sensor = None
        else:
            self._moisture_sensor_pin = moisture_sensor_pin
            self.moisture_sensor = VH400MoistureSensor(self._moisture_sensor_pin)
        self._mcp_pin = mcp_pin
        self.relay = Relay(self._mcp_pin)
        self.moisture_water_threshold = moisture_water_threshold
        self.watering_duration = watering_duration
        self.min_seconds_between_waterings = min_seconds_between_waterings
        if temp_sensor_id in [None, 'None']:
            self.temp_sensor = None
        else:
            self._temp_sensor_id = temp_sensor_id
            self.temp_sensor = TempSensor(self._temp_sensor_id)
        self.temp_scale = temp_scale
        self.state = dict('')
        self.state['last_water_time'] = None
        self.state_file_name = os.path.join(path, '../.%s.pkl' % self.name)
        try:
            sf = open(self.state_file_name, 'r+')
        except IOError:
            sf = open(self.state_file_name, 'w+')
        try:
            self.state = Pickle.load(sf)
        except EOFError:
            self.state['last_water_time'] = None
            Pickle.dump(self.state, sf)

    def water(self):
        """
        Waters a zone
        Returns True if able to water, returns False if unable (last water time is too recent)

        :return: bool
        """
        now = time.time()
        if self.state['last_water_time'] is None:
            self.state['last_water_time'] = now
        if (now == self.state['last_water_time']) or (now - self.state['last_water_time'] > self.min_seconds_between_waterings):
            if DEBUG:
                print("Debug mode, not turning on relay")
            else:
                self.state['last_water_time'] = now
                with open(self.state_file_name, 'r+') as sf:
                    Pickle.dump(self.state, sf)
                self.relay.set_state(self.relay.ON)
            time.sleep(self.watering_duration)
            self.relay.set_state(self.relay.OFF)
            return True
        else:
            with open(self.state_file_name, 'r+') as sf:
                Pickle.dump(self.state, sf)
            print('Not enough time has elapsed since last watering (min: %ss). Not starting watering cycle.' % self.min_seconds_between_waterings)
            return False

    def water_now(self):
        """
        Force a watering cycle regardless of last_water_time

        :return:
        """
        if DEBUG:
            print("Debug mode, not turning on relay")
        else:
            self.state['last_water_time'] = time.time()
            with open(self.state_file_name, 'r+') as sf:
                Pickle.dump(self.state, sf)
            self.relay.set_state(self.relay.ON)
        time.sleep(self.watering_duration)
        self.relay.set_state(self.relay.OFF)

    @property
    def temp(self):
        """
        Returns the temperature in Fahrenheit
        :return:
        """
        if self.temp_sensor is None:
            return None
        else:
            if self.temp_scale.lower() in ['f', 'fahrenheit']:
                return self.temp_sensor.temp_f
            elif self.temp_scale.lower()  in ['c', 'celsius']:
                return self.temp_sensor.temp_c

    @property
    def moisture(self):
        """
        Returns the moisture sensor Volumetric Moisture Content Percentage

        :return: float
        """
        if self.moisture_sensor is None:
            return None
        else:
            return self.moisture_sensor.percent
