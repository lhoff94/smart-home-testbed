import paho.mqtt.client as mqtt #import the client
from datetime import datetime
import time
import sys

print("Started Client", file = sys.stderr)

TOPIC = "home/tutoriallhoff/PubSubDemo"
BROKER_ADDRESS = "mosquittoserver"
PORT = 1883
QOS = 1

if __name__ == "__main__":
    while True:

        client = mqtt.Client()

        client.connect(BROKER_ADDRESS, PORT)

        print("Connected to MQTT Broker: " + BROKER_ADDRESS, file = sys.stdout)

        DATA = dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        client.publish(TOPIC, DATA, qos=QOS)

        client.loop()

        time.sleep(10)
        