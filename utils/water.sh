#!/bin/bash

echo "========================================================="
date
cd /home/pi/prog/garden_pi/utils
sudo PYTHONPATH=/home/pi/prog/garden_pi ./water.py
