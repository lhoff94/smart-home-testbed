import time
import os
import json
from temperature_client import TemperatureClient
from machine import Pin


with open('config.json') as config_file:
    config = json.load(config_file)

try:
    if (os.uname()[0]=='esp32'):
        physical = True
    else:
        physical = False
except AttributeError:
    physical = False

if physical:
    button = Pin(2, Pin.IN, Pin.PULL_UP)
    if button.value():
        time.sleep(20) 
        sensor_temp = TemperatureClient(
        config['mqtt_client_id'],
        config['mqtt_broker'],
        physical,
        config['temp_sensor_pin'],
        False,
        config['mqtt_topic']
            )
    time.sleep(5)
    print('Starting measurment')
#sensor_temp.start()
    while True:
        sensor_temp.publishTemperature()
        time.sleep(config['measure_interval'])