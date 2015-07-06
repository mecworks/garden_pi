#!/usr/bin/env python
# Pretty simple right now, just enough to water on a schedule and log the data

import RPi.GPIO as GPIO
GPIO.setwarnings(False)
from common.zone import Zone
from common.cpu_temp import CpuTemp
from common.temp_sensor import TempSensor
from common.rc_sensor import RcSensor
from common.utils import run_as_thread
from common.utils import format_float
import common.csv_logger as cvs_logger
import ConfigParser
from apscheduler.schedulers.background import BackgroundScheduler
import sys
import signal
import time
import logging
import threading
from threading import Thread

# Config file
config_file = './garden_pi.cfg'
conf_parser = ConfigParser.ConfigParser()
conf_parser.read(config_file)
DEBUG = conf_parser.getboolean('main', 'debug')

# General sensors
ambient_temp_sensor_id = conf_parser.get('main', 'ambient_temp_sensor')
ambient_temp_sensor = TempSensor(ambient_temp_sensor_id)
ambient_light_sensor_gpio = conf_parser.getint('main', 'ambient_light_sensor_gpio')
ambient_light_sensor = RcSensor(gpio=ambient_light_sensor_gpio)
c_temp = CpuTemp()

# Log file
logging.basicConfig()
log_file = conf_parser.get('main', 'logfile')
garden_pi_logger = cvs_logger.CvsLogger('./data/garden_pi.csv')
logger_ID = 'Gargen Pi Logger'
csv_logger = logging.getLogger(logger_ID)

# Initialize zones
zone_names = ['zone_1', 'zone_2', 'zone_3', 'zone_4']
garden_pi_zones = {}
for zone_name in zone_names:
    alias = conf_parser.get(zone_name, 'alias')
    moisture_sensor_gpio = conf_parser.getint(zone_name, 'moisture_sensor_gpio')
    relay_gpio = conf_parser.getint(zone_name, 'relay_gpio')
    moisture_water_threshold = conf_parser.getint(zone_name, 'moisture_water_threshold')
    watering_duration = conf_parser.getint(zone_name, 'watering_duration')
    temp_sensor_id = conf_parser.get(zone_name, 'temp_sensor_id')
    min_seconds_between_waterings = conf_parser.getint(zone_name, 'min_seconds_between_waterings')
    garden_pi_zones[zone_name] = Zone(name=zone_name,
                                  alias=alias,
                                  moisture_sensor_gpio=moisture_sensor_gpio,
                                  relay_gpio=relay_gpio,
                                  moisture_water_threshold=moisture_water_threshold,
                                  watering_duration=watering_duration,
                                  min_seconds_between_waterings=18000,
                                  temp_sensor_id=temp_sensor_id)


class MeasurementData(object):
    
    def __init__(self):
        self._measurements = {'zone_1_moisture': None,
                              'zone_1_temp': None,
                              'zone_2_moisture': None,
                              'zone_2_temp': None,
                              'zone_3_moisture': None,
                              'zone_3_temp': None,
                              'zone_4_moisture': None,
                              'zone_4_temp': None,
                              'ambient_light': None,
                              'ambient_temp': None,
                              'cpu_temp': None}

    def __getitem__(self, item):
        return self._measurements[item]

    def __setitem__(self, key, value):
        self._measurements[key] = value
        
    def reset(self):
        for key in self._measurements.keys():
            self._measurements[key] = None

    @property
    def done(self):
        if None in self._measurements.viewvalues():
            return False

    @run_as_thread
    def get_zone_measurement(self, zone_name, measurement_type):
        assert zone_name in zone_names
        if measurement_type == 'moisture':
            self._measurements[zone_name + '_moisture'] = garden_pi_zones[zone_name].moisture
        elif measurement_type == 'temp':
            self._measurements[zone_name + '_temp'] = garden_pi_zones[zone_name].temp
        else:
            raise ValueError('measurement type %s unsupported' % measurement_type)

    @run_as_thread
    def get_ambient_light(self):
        self._measurements['ambient_light'] = ambient_light_sensor.rc_count()

    @run_as_thread
    def get_ambient_temp(self):
        self._measurements['ambient_temp'] = ambient_temp_sensor.temp_f

    @run_as_thread
    def get_cpu_temp(self):
        self._measurements['cpu_temp'] = c_temp.cpu_temp_f


def log_measurements(measurement_d):
    assert isinstance(measurement_data, MeasurementData)
    measurement_d.reset()
    my_threads = []
    my_threads.append(measurement_d.get_ambient_light())
    my_threads.append(measurement_d.get_ambient_temp())
    my_threads.append(measurement_d.get_cpu_temp())
    my_threads.append(measurement_d.get_zone_measurement('zone_1', 'moisture'))
    my_threads.append(measurement_d.get_zone_measurement('zone_1', 'temp'))
    my_threads.append(measurement_d.get_zone_measurement('zone_2', 'moisture'))
    my_threads.append(measurement_d.get_zone_measurement('zone_2', 'temp'))
    my_threads.append(measurement_d.get_zone_measurement('zone_3', 'moisture'))
    my_threads.append(measurement_d.get_zone_measurement('zone_3', 'temp'))
    my_threads.append(measurement_d.get_zone_measurement('zone_4', 'moisture'))
    my_threads.append(measurement_d.get_zone_measurement('zone_4', 'temp'))
    while True in map(Thread.is_alive, my_threads):
        time.sleep(.1)
    garden_pi_logger.log_csv(zone_1_moisture=measurement_d['zone_1_moisture'],
                             zone_1_temp=measurement_d['zone_1_temp'],
                             zone_2_moisture=measurement_d['zone_2_moisture'],
                             zone_2_temp=measurement_d['zone_2_temp'],
                             zone_3_moisture=measurement_d['zone_3_temp'],
                             zone_3_temp=measurement_d['zone_1_temp'],
                             zone_4_moisture=measurement_d['zone_3_temp'],
                             zone_4_temp=measurement_d['zone_4_temp'],
                             ambient_light=measurement_d['ambient_light'],
                             ambient_temp=measurement_d['ambient_temp'],
                             cpu_temp=measurement_d['cpu_temp'])

def water_zone(zone_name):
    s = time.time()
    garden_pi_logger.log_csv(messg='START WATERING: %s' % zone_name.upper())
    garden_pi_zones[zone_name].water()
    f = time.time()
    garden_pi_logger.log_csv(messg='END WATERING: %s. Elapsed Time: %ss' % (zone_name.upper(), format_float(f-s)))

def cleanup(force_exit=False):
    scheduler.shutdown(wait=False)
    GPIO.cleanup()
    garden_pi_logger.log_csv(messg="SHUTTING DOWN")
    if force_exit is True:
        sys.exit(0)


def signal_handler(signal, frame):
    """
    Handle Ctrl-C

    :param signal:
    :param frame:
    :return:
    """
    print '\nCtrl-C detected, cleaning up...'
    cleanup(force_exit=True)


print('Starting Garden Pi')
signal.signal(signal.SIGINT, signal_handler)
scheduler = BackgroundScheduler()
measurement_data = MeasurementData()
scheduler.add_job(log_measurements, args=[measurement_data], trigger='interval', minutes=1, name='Data Logger', id='data_logger', max_instances=1, misfire_grace_time=20)
for zone_name in garden_pi_zones.keys():
    #scheduler.add_job(water_zone, trigger='cron', hour='7,18', minute=15, name=zone, max_instances=1, misfire_grace_time=20)
    scheduler.add_job(water_zone, trigger='cron', args=[zone_name], name=zone_name, minute='*/5', max_instances=1, misfire_grace_time=20)
scheduler.start()
for job in scheduler.get_jobs():
    print("Job: %s, Func: %s, Next run time: %s" % (job.name, job.func_ref, job.next_run_time))
while True:
    time.sleep(1)

cleanup()
