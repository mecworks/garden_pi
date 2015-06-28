#!/usr/bin/env python

# A CVS logger for garden pi

import logging
import logging.handlers
from common.utils import format_float
import os

class CvsLogger(object):

    def __init__(self, log_file_name):
        pass
        self.header = 'TIMESTAMP, ZONE, ALIAS, AMBIENT TEMP, AMBIENT LIGHT, SOIL MOISTURE, SOIL TEMP, CPU TEMP, MESSG\n'
        self.logger_ID = 'Gargen Pi Logger'
        self.log_file = log_file_name
        self.log_level = logging.INFO
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
        self.csv_logger_fh.setLevel(self.log_level)
        self.csv_logger_formatter = logging.Formatter('%(message)s')
        self.csv_logger_fh.setFormatter(self.csv_logger_formatter)
        self.csv_logger.addHandler(self.csv_logger_fh)


    def log_csv(self, timestamp=None, v1_05=None, v1_5=None, v1_8=None, v3_3=None, v5_0=None, curr=None, vid=None, spg=None, trans_t=None, heat_sink_t=None, messg=" "):
        """
        Log a message to the CSV log file

        TIMESTAMP, PASS, VOLT, FREQ,  1_05V, 1_5V, 1_8V, 3_3V, 5_0V, CURR, VID, SPG, RENCO_TRANS, HEAT_SINK, MESSG\n

        :param timestamp:
        :param v1_05:
        :param v1_5:
        :param v1_8:
        :param v3_3:
        :param v5_0:
        :param curr:
        :param vid:
        :param spg:
        :param trans_t:
        :param heat_sink_t:
        :param messg:
        :return:
        """
        fmt = '{0:.5f}'
        if timestamp is None:
            timestamp = ts()
        v1_05 = format_float(v1_05)
        v1_5 = format_float(v1_5)
        v1_8 = format_float(v1_8)
        v3_3 = format_float(v3_3)
        v5_0 = format_float(v5_0)
        curr = format_float(curr)
        vid = format_float(vid)
        spg = format_float(spg)
        trans_t = format_float(trans_t)
        heat_sink_t = self.format_float(heat_sink_t)
        log_msg = '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s' % \
                  (timestamp,
                   self.current_iter,
                   self.current_voltage,
                   self.current_freq,
                   v1_05,
                   v1_5,
                   v1_8,
                   v3_3,
                   v5_0,
                   curr,
                   vid,
                   spg,
                   trans_t,
                   heat_sink_t,
                   messg)
        self.csv_logger.info(log_msg)


        def log_temps(self):
        """
        Log temperatures

        Add as a scheduled job using apscheduler
        """
        renco_transformer = self.temp_sensors['renco_transformer'].get_c()
        heatsink_near_reg = self.temp_sensors['heatsink_near_reg'].get_c()
        self.log_csv(trans_t=renco_transformer,
                     heat_sink_t=heatsink_near_reg)