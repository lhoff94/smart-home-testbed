import time


class sensor:

    def __init__(self):
        from machine import Pin, SoftI2C
        pass


    def read():
        pass


class light_sensor(sensor):

    def __init__(self, scl, sda, addr=0x23):
        """
        Initializes a bh1750 pressure sensor
        :param scl: pin number of the serial clock line for the i2c interface
        :param sda: pin number of the serial data line for the i2c interface
        :param addr: i2c adreess, 0x23 is default, if addr pin is pulled high it is 0x5c
        """
        super().__init__()
        from bh1750 import BH1750
        self.i2c = SoftI2C(scl=Pin(scl), sda=Pin(sda),)
        self.sensor = BH1750(self.i2c, addr)
    
    def read(self):
        return self.sensor.luminance(BH1750.ONCE_HIRES_1)


class pressure_sensor(sensor):

    def __init__(self, scl, sda):
        """
        Initializes a bmp180 pressure sensor
        :param scl: pin number of the serial clock line for the i2c interface
        :param sda: pin number of the serial data line for the i2c interface
        """
        super().__init__()
        from bmp180 import BMP180
        self.i2c = SoftI2C(scl=Pin(scl), sda=Pin(sda), freq=100000)
        self.sensor = BMP180(self.i2c)
        self.sensor.oversample_sett = 2

    def read(self, unit="p"):
        if unit == "P":
            return self.sensor.pressure
        elif unit == "hP" or unit == "mbar":
            return self.sensor.pressure/100
        elif unit == "Bar":
            return self.sensor.pressure/100000
        else:
            raise ValueError("Unknown unit, use P, hP, mbar or Bar") 

    
    def read_temp(self):
        # The bmp180 has a additional temperature sensor, since its not the primary use
        # case its not exposed via the "read" function but a additional function
        """
        Measures Temperature and returns in celsius
        """
        return self.sensor.temp

class co2_sensor(sensor):

    def __init__(self, uart):
        from mhz19 import mhz19
        super().__init__()
        self.sensor = mhz19(uart)
    
    def read(self):
        self.sensor.get_data()
        return self.sensor.ppm
    
    def read_temp(self):
        # The mhz19 has a additional temperature sensor, since its not the primary use
        # case its not exposed via the "read" function but a additional function
        """
        Measures Temperature and returns in celsius
        """
        self.sensor.get_data()
        return self.sensor.temp

class temperature_sensor(sensor):

    def __init__(self, pin):
        super().__init__()
        from ds18x20 import DS18X20
        from onewire import OneWire
        self.sensor = DS18X20(OneWire(Pin(pin)))
        sensor_addrs = self.sensor.scan()
        if not sensor_addrs:
            raise Exception('no DS18B20 found at bus on pin %d' % pin)
        self.sensor_addr = sensor_addrs.pop()
    
    def read(self):
        self.sensor.convert_temp()
        time.sleep_ms(750)
        return self.sensor.read_temp(self.sensor_addr)


class mock_sensor(sensor):
    
    def __init__(self, base_addr, sensor_type):
        import urequests
        self.addr = base_addr + "berlin"

    def read(self):
        response = urequests.get(self.addr).json()
        return(response["temperature"])
    






