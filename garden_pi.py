#!/usr/bin/env python
# Pretty simple right now, just enough to water on a schedule and log the data

from common.zone import Zone
from common.cpu_temp import CpuTemp
from common.temp_sensor import TempSensor
from common.utils import run_as_thread
from common.utils import format_float
import common.csv_logger as cvs_logger
import ConfigParser
from apscheduler.schedulers.background import BackgroundScheduler
import sys
import signal
import time
import logging
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
ambient_light_sensor = None  # TODO: We have no ambient light sensor until the tsl2561 sensor is working.  For now, output a space.
c_temp = CpuTemp()
temp_scale = conf_parser.get('main', 'temp_scale')
if temp_scale.lower() not in ['f', 'fahrenheit', 'c', 'celsius']:
    raise ValueError("temp_scale value must be one of 'f', 'fahrenheit', 'c' or 'celsius' (case insensitive)")

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
    moisture_sensor_pin = conf_parser.getint(zone_name, 'moisture_sensor_pin')
    mcp_relay_pin = conf_parser.getint(zone_name, 'relay_gpio')
    moisture_water_threshold = conf_parser.getint(zone_name, 'moisture_water_threshold')
    watering_duration = conf_parser.getint(zone_name, 'watering_duration')
    temp_sensor_id = conf_parser.get(zone_name, 'temp_sensor_id')
    min_seconds_between_waterings = conf_parser.getint(zone_name, 'min_seconds_between_waterings')
    garden_pi_zones[zone_name] = Zone(name=zone_name,
                                      alias=alias,
                                      moisture_sensor_pin=moisture_sensor_pin,
                                      mcp_pin=mcp_relay_pin,
                                      moisture_water_threshold=moisture_water_threshold,
                                      watering_duration=watering_duration,
                                      min_seconds_between_waterings=min_seconds_between_waterings,
                                      temp_sensor_id=temp_sensor_id,
                                      temp_scale=temp_scale)


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
        #self._measurements['ambient_light'] = ambient_light_sensor.rc_count()
        self._measurements['ambient_light'] = 0  # TODO: We have no ambient light sensor until the tsl2561 sensor is working.  For now, output a 0.

    @run_as_thread
    def get_ambient_temp(self):
        global temp_scale
        if temp_scale.lower() in ['f', 'fahrenheit']:
            self._measurements['ambient_temp'] = ambient_temp_sensor.temp_f
        elif temp_scale.lower() in ['c', 'celsius']:
            self._measurements['ambient_temp'] = ambient_temp_sensor.temp_c

    @run_as_thread
    def get_cpu_temp(self):
        global temp_scale
        if temp_scale.lower() in ['f', 'fahrenheit']:
            self._measurements['cpu_temp'] = c_temp.cpu_temp_f
        elif temp_scale.lower() in ['c', 'celsius']:
            self._measurements['cpu_temp'] = c_temp.cpu_temp_c


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
                             zone_3_moisture=measurement_d['zone_3_moisture'],
                             zone_3_temp=measurement_d['zone_3_temp'],
                             zone_4_moisture=measurement_d['zone_4_moisture'],
                             zone_4_temp=measurement_d['zone_4_temp'],
                             ambient_light=measurement_d['ambient_light'],
                             ambient_temp=measurement_d['ambient_temp'],
                             cpu_temp=measurement_d['cpu_temp'])


def water_zone(zone_name, force_water=False):
    """
    Trigger watering of a zone by moisture sensor

    :param zone_name: The name of the zone as used in the zone section header in the config file (i.e. 'zone_1', 'zone_4')
    :type zone_name: str
    """
    water = False
    msg = ' '
    if (garden_pi_zones[zone_name].seconds_before_ok_to_water == 0) and (garden_pi_zones[zone_name].moisture < garden_pi_zones[zone_name].moisture_water_threshold):
        water = True
        msg = 'MOISTURE SENSOR'
    if force_water is True:
        water = True
        msg = 'IMMEDIATE'
    if water is True:
        s = time.time()
        garden_pi_logger.log_csv(messg='START WATERING (%s): %s' % (msg, zone_name.upper()))
        garden_pi_zones[zone_name].water()
        f = time.time()
        garden_pi_logger.log_csv(messg='END WATERING (%s): %s. Elapsed Time: %ss' % (msg, zone_name.upper(), format_float(f-s)))



def cleanup(force_exit=False):
    scheduler.shutdown(wait=False)
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
#scheduler.add_job(log_measurements, args=[measurement_data], trigger='cron', minute='*/5', name='Data Logger', id='data_logger', max_instances=1, misfire_grace_time=20)
scheduler.add_job(log_measurements, args=[measurement_data], trigger='cron', minute='*', name='Data Logger', id='data_logger', max_instances=1, misfire_grace_time=20)
for zone_name in garden_pi_zones.keys():
    #scheduler.add_job(water_zone, trigger='cron', hour='7,18', minute=15, args=[zone_name], name=zone_name, max_instances=1, misfire_grace_time=20)
    scheduler.add_job(water_zone, trigger='cron', minute="*", args=[zone_name], name=zone_name, max_instances=1, misfire_grace_time=20)
scheduler.start()
for job in scheduler.get_jobs():
    print("Job: %s, Func: %s, Next run time: %s" % (job.name, job.func_ref, job.next_run_time))
    sys.stdout.flush()

while True:
    time.sleep(1)

cleanup()
