#!/bin/bash



for DIR in $(ls -d /sys/bus/w1/devices/28*);
do
   t=$(cat $DIR/w1_slave | grep t= | sed -e 's/.*t=\(..\)\(...\)/\1\.\2/')
   t_f=$(echo "scale=2;((9/5) * $t) + 32" |bc)
   echo "$(basename $DIR): $t_f"
done
cpu_temp_c=$(vcgencmd measure_temp | sed -e 's/temp=\(.*\).C/\1/')
cpu_temp_f=$(echo "scale=2;((9/5) * $cpu_temp_c) + 32" |bc)
echo "CPU temp: $cpu_temp_f"
