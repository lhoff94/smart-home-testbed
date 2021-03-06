# DS18x20 temperature sensor driver for MicroPython.
# MIT license; Copyright (c) 2016 Damien P. George

import urequests
import json


class DS18X20:
    def __init__(self, onewire):
        self.onewire = onewire
        with open('config.json') as config_file:
            config = json.load(config_file)
        self.endpoint = f"{config['mock_endpoint']}{config['sensor_name']}/"
        return None

    def scan(self):
        # Returns False so that probe if sensor was found still passes
        return [True]

    def convert_temp(self):
        return 1

    def read_temp(self, rom):
        '''
        Temperature in degree C.
        '''
        response = urequests.get(self.endpoint + 'Temperature').json()
        return(response)

