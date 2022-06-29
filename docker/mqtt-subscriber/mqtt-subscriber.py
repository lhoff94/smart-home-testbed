import paho.mqtt.client as mqtt
import time
import sys

TOPIC = "home/tutoriallhoff/PubSubDemo"
BROKER_ADDRESS = "mosquittoserver"
PORT = 1883

time.sleep(30)


def on_message(client, userdata, message):
    msg = str(message.payload.decode("utf-8"))
    print("message topic: ", message.topic, file = sys.stderr)
    print("message received: ", msg, file = sys.stderr)


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker: " + BROKER_ADDRESS, file = sys.stderr)
    client.subscribe(TOPIC)

if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER_ADDRESS, PORT)

    client.loop_forever()