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
    if button:
        time.sleep(20) 
        sensor1 = TemperatureClient(
            config['mqtt_client_id'],
            config['mqtt_broker'],
            physical,
            config['temp_sensor_pin'],
            False,
            config['mqtt_topic']
            )
        time.sleep(5)
        print('Starting temperatur measurment')
        sensor1.start()

