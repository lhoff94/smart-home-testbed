import paho.mqtt.client as mqtt

TOPIC = "home/tutoriallhoff/PubSubDemo"
BROKER_ADDRESS = "10.0.0.2"
PORT = 1883

def on_message(client, userdata, message):
    msg = str(message.payload.decode("utf-8"))
    print("message topic: ", message.topic)
    print("message received: ", msg)


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker: " + BROKER_ADDRESS)
    client.subscribe(TOPIC)

if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER_ADDRESS, PORT)

    client.loop_forever()