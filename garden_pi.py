#!/usr/bin/env python
# Pretty simple right now, just enough to water on a schedule and log the data

from common.zone import Zone
from common.cpu_temp import CpuTemp
from common.temp_sensor import TempSensor
from common.rc_sensor import RcSensor
import common.csv_logger as cvs_logger
import ConfigParser
import ast
from apscheduler.schedulers.background import BackgroundScheduler

# Config file
config_file = './garden_pi.cfg'
conf_parser = ConfigParser.ConfigParser()
conf_parser.read(config_file)

# General sensors
ambient_temp_sensor_id = conf_parser.get('Main', 'ambient_temp_sensor')
ambient_temp_sensor = TempSensor(ambient_temp_sensor_id)
ambient_light_sensor_gpio = conf_parser.get('Main', 'ambient_light_sensor_gpio')
ambient_light_sensor = RcSensor(gpio=ambient_light_sensor_gpio)
c_temp = CpuTemp()

# Log file
log_file = conf_parser.get('Main', 'log_file')
garden_pi_logger = cvs_logger.CvsLogger('./data/garden_pi.csv')

# Initialize zones
zone_names = ['Zone 1', 'Zone 2', 'Zone 3', 'Zone 4']
garden_pi_zones = {}
for _zone in zone_names:
    alias = conf_parser.get(_zone, 'alias')
    moisture_sensor_gpio = conf_parser.get(_zone, 'moisture_sensor_gpio')
    relay_gpio = conf_parser.get(_zone, 'relay_gpio')
    moisture_water_threshold = conf_parser.get(_zone, 'moisture_water_threshold')
    watering_duration = conf_parser.get(_zone, 'watering_duration')
    temp_sensor_id = conf_parser.get(_zone, 'temp_sensor_id')
    min_seconds_between_waterings = conf_parser.get(_zone, 'min_seconds_between_waterings')
    garden_pi_zones[_zone] = Zone(alias=alias,
                                  moisture_sensor_gpio=moisture_sensor_gpio,
                                  relay_gpio=relay_gpio,
                                  moisture_water_threshold=moisture_water_threshold,
                                  watering_duration=watering_duration,
                                  min_seconds_between_waterings=18000,
                                  temp_sensor_id=temp_sensor_id)


def log_measurements():
    zone_1_moisture = garden_pi_zones['Zone 1'].moisture
    zone_1_temp = garden_pi_zones['Zone 1'].temp
    zone_2_moisture = garden_pi_zones['Zone 2'].moisture
    zone_2_temp = garden_pi_zones['Zone 2'].temp
    zone_3_moisture = garden_pi_zones['Zone 3'].moisture
    zone_3_temp = garden_pi_zones['Zone 3'].temp
    zone_4_moisture = garden_pi_zones['Zone 4'].moisture
    zone_4_temp = garden_pi_zones['Zone 4'].temp
    ambient_light = ambient_light_sensor.rc_count()
    ambient_temp = ambient_temp_sensor.get_f()
    cpu_temp = c_temp.cpu_temp_f
    garden_pi_logger.log_csv(zone_1_moisture=zone_1_moisture,
                             zone_1_temp=zone_1_temp,
                             zone_2_moisture=zone_2_moisture,
                             zone_2_temp=zone_2_temp,
                             zone_3_moisture=zone_3_moisture,
                             zone_3_temp=zone_3_temp,
                             zone_4_moisture=zone_4_moisture,
                             zone_4_temp=zone_4_temp,
                             ambient_light=ambient_light,
                             ambient_temp=ambient_temp,
                             cpu_temp=cpu_temp)

def water_zone(zone_object):
    pass

scheduler = BackgroundScheduler()
scheduler.add_job(log_voltages, trigger='interval', seconds=1, name='Voltage Logger', id='voltage_logger', max_instances=1)
scheduler.add_job(log_measurements, trigger='interval', minutes=5, name='Data Logger', id='data_logger', max_instances=1)
scheduler.add_job(log_current, name='Log Current', id='log_current')
scheduler.start()