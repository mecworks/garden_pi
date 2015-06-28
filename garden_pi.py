#!/usr/bin/env python

# The main program that tracks data, monitors zones and schedules watering and logging facilities
#
# Sensor GPIOs:
# PIN    GPIO
# 13     21/27
# 15     22
# 16     23
# 18     24
#
# Relays:
# 5      3
# 8      14
# 10     15
# 11     17

import common.zone as zone