import time


class TemperatureSensor:
    """
    Represents a Temperature sensor
    """

    def __init__(self, pin, physical):
        """
        Finds address of single DS18B20 on bus specified by `pin`
        :param pin: 1-Wire bus pin
        :type pin: int
        :type physical: Bool
        """
        #Only Import libraries if script runs on physical hardware
        self.physical = physical
        if physical:
            from ds18x20 import DS18X20
            from machine import Pin
            from onewire import OneWire
            self.ds = DS18X20(OneWire(Pin(pin)))
            addrs = self.ds.scan()
            if not addrs:
                raise Exception('no DS18B20 found at bus on pin %d' % pin)
            # save what should be the only address found
            self.addr = addrs.pop()
            

    def read_temp(self, fahrenheit=False):
        """
        Reads temperature from a single DS18X20
        :param fahrenheit: Whether or not to return value in Fahrenheit
        :type fahrenheit: bool
        :return: Temperature
        :rtype: float
        """
        if self.physical:
            self.ds.convert_temp()
            time.sleep_ms(750)
            temp = self.ds.read_temp(self.addr)
            if fahrenheit:
                return self.c_to_f(temp)
        else:
            import urequests
            response = urequests.get('http://host:8080/temperature/berlin').json()
            return(response["temperature"])
        return temp

    @staticmethod
    def c_to_f(c):
        """
        Converts Celsius to Fahrenheit
        :param c: Temperature in Celsius
        :type c: float
        :return: Temperature in Fahrenheit
        :rtype: float
        """
        return (c * 1.8) + 32