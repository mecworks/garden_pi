#!/bin/bash
#set -x

BASE_DIR='/home/pi/prog/garden_pi'
LOG_DIR="${BASE_DIR}/data"
LOG_FILE_NAME='garden_pi-cron.csv'
LOG_FILE="${LOG_DIR}/${LOG_FILE_NAME}"

SENSOR_CMD="sudo $BASE_DIR/utils/rcsensor_cli"

if [ ! -f "${LOG_FILE}" ]; then
    touch "${LOG_FILE}"
    echo "TIMESTAMP, ZONE 1 MOISTURE, ZONE 1 TEMP, ZONE 2 MOISTURE, ZONE 2 TEMP, ZONE 3 MOISTURE, ZONE 3 TEMP, ZONE 4 MOISTURE, AMBIETN LIGHT, AMBIENT_TEMP, CPU TEMP" > $LOG_FILE
fi

ts(){
    printf "%.4f\n" $(date +%s.%N)
}

get_temp(){
    DIR="/sys/bus/w1/devices/${1}"
    t=$(cat $DIR/w1_slave | grep t= | sed -e 's/.*t=\(..\)\(...\)/\1\.\2/')
    t_f=$(echo "scale=2;((9/5) * $t) + 32" |bc)
    echo $t_f 
}

log_data() {
    timestamp=$(ts)
    zone_1m=$($SENSOR_CMD -g 22)
    zone_2m=$($SENSOR_CMD -g 23)
    zone_3m=$($SENSOR_CMD -g 24)
    zone_4m=$($SENSOR_CMD -g 25)
    zone_1t=$(get_temp 28-000005760fd1)
    zone_2t=$(get_temp 28-000005f7fe06)
    zone_3t=$(get_temp 28-000005f8081d)
    ambient_t=$(get_temp 28-000005f8d181)
    light=$($SENSOR_CMD -g 21)
    cpu_temp_c=$(vcgencmd measure_temp | sed -e 's/temp=\(.*\).C/\1/')
    cpu_temp_f=$(echo "scale=2;((9/5) * $cpu_temp_c) + 32" |bc)
    echo "$timestamp, $zone_1m, $zone_1t, $zone_2m, $zone_2t, $zone_3m, $zone_3t, $zone_4m, $light, $ambient_t, $cpu_temp_f" >> $LOG_FILE
}

log_data
