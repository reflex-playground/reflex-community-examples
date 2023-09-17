import network
import time
from machine import Pin
from umqtt.simple import MQTTClient


buttonPin = Pin(18, Pin.IN) # D2 Pin: detect the button clicking
outputPin = Pin(5, Pin.OUT)  
outputPin.value(1) 


# MQTT Server Parameters
MQTT_CLIENT_ID = "my_pico_mqtt_client"
MQTT_BROKER    = "broker.emqx.io"
MQTT_USER      = ""
MQTT_PASSWORD  = ""
MQTT_TOPIC     = "MiloTopic"

print("Connecting to WiFi", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Wokwi-GUEST', '')
while not sta_if.isconnected():
  print(".", end="")
  time.sleep(0.1)
print(" Connected!")

print("Connecting to MQTT server... ", end="")
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD)
client.connect()

print("Connected!")

while True:
  if buttonPin.value() == 1:
    client.publish(MQTT_TOPIC, "add")
  time.sleep(1)
