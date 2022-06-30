from email.headerregistry import ContentTransferEncodingHeader
import time
import os
import json

from uvicorn import Config
from temperature_client import TemperatureClient
from machine import Pin
from mqtt import MQTTClient

import sensors


def measure(sensor_list):
    client = MQTTClient(config['mqtt_client_id'], config['mqtt_broker'], config['mqtt_port'])
    client.connect()


    while True:
        print("Sending measurements")
        for sensor in sensor_list:
            client.publish(config['mqtt_topic']+ "/" + sensor[0], str(sensor[1].read()))
        time.sleep(config['measure_interval'])


with open('config.json') as config_file:
    config = json.load(config_file)

try:
    if (os.uname()[0]=='esp32'):
        physical = True
    else:
        physical = False
except AttributeError:
    physical = False

button = Pin(2, Pin.IN, Pin.PULL_UP)
if button.value():
    sensor_list = []
    sensor_list.append(['luminance',sensors.light_sensor(scl=22, sda=21)])
    sensor_list.append(['pressure',sensors.pressure_sensor(scl=5, sda=4)])
    sensor_list.append(['co2level',sensors.co2_sensor(2)])
    sensor_list.append(['temperature', sensors.temperature_sensor(config['temp_sensor_pin'])])
  
    measure(sensor_list)


#if physical:
#    pass




    

#time.sleep(5)
#print('Starting measurment')
#sensor_temp.start()
#    while True:
#        sensor_temp.publishTemperature()
#        time.sleep(config['measure_interval'])




##config['mqtt_client_id'],
  ##      config['mqtt_broker'],
    ##    physical,
      ##  config['temp_sensor_pin'],
        ##False,
        ##config['mqtt_topic']