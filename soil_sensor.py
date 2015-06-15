#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

# Sensor GPIOs:
# PIN    GPIO
# 13     21/27
# 15     22
# 16     23
# 18     24
#
# relays:
# 5      3
# 8      14
# 10     15
# 11     17

file = open("SensorData.txt", "w") #stores data file in same directory as this program file

#Define function to measure charge time
def RC_Analog(gpio):
    print('In RC_Analog')
    print('GPIO: %s' % gpio)
    #Discharge capacitor
    print('Discharging cap')
    GPIO.setup(gpio, GPIO.OUT)
    GPIO.output(gpio, GPIO.LOW)
    time.sleep(0.1) #in seconds, suspends execution.
    print('Starting charge cycle')
    start_time = time.time()
    GPIO.setup(gpio, GPIO.IN)
    while (GPIO.input(gpio)==GPIO.LOW):
        pass
    # GPIO.setup(gpio, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
    # GPIO.wait_for_edge(gpio, GPIO.RISING)
    end_time = time.time()
    print('Difference: %s' % str(end_time - start_time))
    return end_time - start_time

    #Main program loop
while True:
    time.sleep(1)
    ts = time.time()
    reading = RC_Analog(24) #store counts in a variable
    counter = 0
    time_start = 0
    time_end = 0

    print ts, reading  #print counts using GPIO4 and time
    file.write(str(ts) + " " + str(reading) + "\n") #write data to file

    while (reading < 10.00):
        time_start = time.time()
        counter = counter + 1
        if counter >= 50:
            break
    time_end = time.time()
    if (counter >= 25 and time_end - time_start <= 60): # if you get 25 measurements that indicate dry soil in less than one minute, need to water
        print('Not enough water for your plants to survive! Please water now.') #comment this out for testing
#    else:
 #     print('Your plants are safe and healthy, yay!')

GPIO.cleanup()
file.close()

