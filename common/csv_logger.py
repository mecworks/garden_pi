#!/usr/bin/env python

# A CVS logger for garden pi

import logging
import logging.handlers
from common.utils import format_float
from common.utils import timestamp as ts
import os

class CvsLogger(object):

    def __init__(self, log_file_name):
        pass
        self.header = "TIMESTAMP, ZONE 1 MOISTURE, ZONE 1 TEMP, ZONE 2 MOISTURE, ZONE 2 TEMP, ZONE 3 MOISTURE, ZONE 3 TEMP, ZONE 4 MOISTURE, AMBIENT LIGHT, AMBIENT TEMP, CPU TEMP, MESSAGE\n"
        self.logger_ID = 'Gargen Pi Logger'
        self.csv_logger = None
        self.log_file = log_file_name
        self.log_level = logging.DEBUG
        self._configure_cvs_logger()

    def _configure_cvs_logger(self):
        """
        Configure our logging
        """
        # If the file doesn't exist, lay down a column header
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w') as f:
                f.write(self.header)
        self.csv_logger = logging.getLogger(self.logger_ID)
        self.csv_logger_fh = logging.FileHandler(self.log_file)
        self.csv_logger_formatter = logging.Formatter('%(message)s')
        self.csv_logger_fh.setFormatter(self.csv_logger_formatter)
        self.csv_logger.addHandler(self.csv_logger_fh)
        self.csv_logger.setLevel(self.log_level)

    def log_csv(self, timestamp=None, zone_1_moisture=None,
                zone_1_temp=None, zone_2_moisture=None,
                zone_2_temp=None, zone_3_moisture=None,
                zone_3_temp=None, zone_4_moisture=None,
                zone_4_temp=None, ambient_light=None,
                ambient_temp=None, cpu_temp=None, messg=" "):
        """
        Log values to a CSV file

        :param timestamp: Timestamp
        :type timestamp: float
        :param zone_1_moisture:
        :type zone_1_moisture: float
        :param zone_1_temp:
        :type zone_1_temp: float
        :param zone_2_moisture:
        :type zone_2_moisture: float
        :param zone_2_temp:
        :type zone_2_temp: float
        :param zone_3_moisture:
        :type zone_3_moisture: float
        :param zone_3_temp:
        :type zone_3_temp: float
        :param zone_4_moisture:
        :type zone_4_moisture: float
        :param zone_4_temp:
        :type zone_4_temp: float
        :param ambient_light:
        :type ambient_light: float
        :param ambient_temp:
        :type ambient_temp: float
        :param cpu_temp:
        :type cpu_temp: float
        :param messg:
        :type messg: str
        """

        if timestamp is None:
            timestamp = ts()
        z1_m = format_float(zone_1_moisture)
        z1_t = format_float(zone_1_temp)
        z2_m = format_float(zone_2_moisture)
        z2_t = format_float(zone_2_temp)
        z3_m = format_float(zone_3_moisture)
        z3_t = format_float(zone_3_temp)
        z4_m = format_float(zone_4_moisture)
        z4_t = format_float(zone_4_temp)
        a_l = format_float(ambient_light)
        a_t = format_float(ambient_temp)
        c_t = format_float(cpu_temp)
        log_msg = '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s %s' % \
                  (timestamp,
                   z1_m,
                   z1_t,
                   z2_m,
                   z2_t,
                   z3_m,
                   z3_t,
                   z4_m,
                   z4_t,
                   a_l,
                   a_t,
                   c_t,
                   messg)
        self.csv_logger.info(log_msg)


if __name__ == '__main__':
    logfile_name = './test.csv'
    my_logger = CvsLogger(logfile_name)
    my_logger.log_csv(messg='Test')

