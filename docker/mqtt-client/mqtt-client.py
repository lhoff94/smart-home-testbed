import paho.mqtt.client as mqtt #import the client

broker_address="mosquitto" 

client = mqtt.Client("P1") #create new instance
client.connect(broker_address) #connect to broker
client.publish("test/test1","ON")#publish