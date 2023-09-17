# refer projects
# https://wokwi.com/projects/305568836183130690 <- OLED display


import network
import time
from machine import Pin, I2C
import ssd1306
from umqtt.simple import MQTTClient


# OLED display
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
oled.text('Hello, Wokwi!', 10, 10)      
oled.show()


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
