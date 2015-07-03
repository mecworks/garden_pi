#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import sys
import signal
from common.utils import progress_bar
import ConfigParser

# Config file
config_file = '../garden_pi.cfg'
conf_parser = ConfigParser.ConfigParser()
conf_parser.read(config_file)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
ON = GPIO.LOW
OFF = GPIO.HIGH
zone_1_gpio = conf_parser.getint('Zone 1', 'relay_gpio')
zone_2_gpio = conf_parser.getint('Zone 2', 'relay_gpio')
zone_3_gpio = conf_parser.getint('Zone 3', 'relay_gpio')
zone_4_gpio = conf_parser.getint('Zone 4', 'relay_gpio')
for zone_gpio in [zone_1_gpio, zone_2_gpio, zone_3_gpio, zone_4_gpio]:
    GPIO.setup(zone_gpio, GPIO.OUT)
    GPIO.output(zone_gpio, OFF)
z1_watering_duration = conf_parser.getint('Zone 1', 'watering_duration')
z2_watering_duration = conf_parser.getint('Zone 2', 'watering_duration')
z3_watering_duration = conf_parser.getint('Zone 3', 'watering_duration')
z4_watering_duration = conf_parser.getint('Zone 4', 'watering_duration')


def water_time(zone_gpio):
    s = time.time()
    GPIO.output(zone_gpio, ON)
    raw_input("Press 'ENTER' when ready to stop")
    GPIO.output(zone_gpio, OFF)
    f = time.time()
    print("Time: %s" % str(f - s))


def water_zone(zone_gpio, t):
    GPIO.output(zone_gpio, ON)
    progress_bar(progress_bar_time=t)
    GPIO.output(zone_gpio, OFF)


def cleanup(force_exit=False):
    GPIO.output(zone_1_gpio, OFF)
    GPIO.output(zone_2_gpio, OFF)
    GPIO.output(zone_3_gpio, OFF)
    GPIO.output(zone_4_gpio, OFF)
    GPIO.cleanup()
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


signal.signal(signal.SIGINT, signal_handler)
# print("Sleeping 30 seconds")
# time.sleep(30)
print("Watering zone 1 for %s seconds." % z1_watering_duration)
water_zone(zone_1_gpio, z1_watering_duration)
print("Watering zone 2 for %s seconds." % z2_watering_duration)
water_zone(zone_2_gpio, z2_watering_duration)
print("Watering zone 3 for %s seconds." % z3_watering_duration)
water_zone(zone_3_gpio, z3_watering_duration)
print("Watering zone 4 for %s seconds." % z4_watering_duration)
water_zone(zone_4_gpio, z4_watering_duration)
print("Done")
cleanup()
