#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from common.utils import format_float

class TempSensor(object):
    """
    A Dallas one-wire temp sensor object for the Raspberry Pi DS18B20
    """

    base_dir = '/sys/bus/w1/devices/'

    def __init__(self, device_id):
        self.sensorID = device_id
        self.device_file = self.base_dir + self.sensorID + '/w1_slave'

    def _read_temp_raw(self):
        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def _read_temp(self):
            lines = self._read_temp_raw()
            while lines[0].strip()[-3:] != 'YES':
                time.sleep(0.2)
                lines = self._read_temp_raw()
            equals_pos = lines[1].find('t=')
            if equals_pos != -1:
                temp_string = lines[1][equals_pos + 2:]
                temp_c = float(temp_string) / 1000.0
                temp_f = temp_c * 9.0 / 5.0 + 32.0
                return temp_c, temp_f

    def get_f(self):
        """
        Get temperature in Fahrenheit

        :return:
        """
        return self._read_temp()[1]

    @property
    def temp_f(self):
        """
        Fahrenheit temp property

        :return:
        """
        return self._read_temp()[1]

    def get_c(self):
        """
        Get temperature in Celsius

        :return:
        """
        return self._read_temp()[0]

    @property
    def temp_c(self):
        """
        Celsius temp property
        :return:
        """
        return self._read_temp()[0]

if __name__ == '__main__':
    import subprocess
    import os
    file_glob = '/sys/bus/w1/devices/28*'
    process = subprocess.Popen(['ls -d %s' % file_glob], stdout=subprocess.PIPE, shell=True)
    out, err = process.communicate()
    file_list = out.split('\n')[:-1]
    ids = map(os.path.basename, file_list)
    sensors = {}
    for id in ids:
        sensors[id] = TempSensor(id)

    for sensor in sensors.keys():
        f = sensors[sensor].get_f()
        c = sensors[sensor].get_c()
        print(u'ID: %s: Temp: %s\xb0F, %s\xb0C' % (sensor, format_float(f), format_float(c)))
    print('')

