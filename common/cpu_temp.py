#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pexpect
import re

class CpuTemp(object):

    def __init__(self):
        self.temp_cmd = '/usr/bin/vcgencmd measure_temp'
        self.temp_re = re.compile('temp=(\d+\.\d+)\D*')

    @property
    def cpu_temp_f(self):
        m = self.temp_re.match(pexpect.run(self.temp_cmd))
        t = float(m.groups()[0])
        t_f = (t * 1.8) + 32
        return t_f

    @property
    def cpu_temp_c(self):
        m = self.temp_re.match(pexpect.run(self.temp_cmd))
        t_c = float(m.groups()[0])
        return t_c


if __name__ == '__main__':
    cpu = CpuTemp()
    print('CPU Temp: \n')
    print(u'   %s\xb0C' % cpu.cpu_temp_c)
    print(u'   %s\xb0F' % cpu.cpu_temp_f)
    print('')