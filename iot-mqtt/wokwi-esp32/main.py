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


def displayView(line1:str='', line2:str='', line3:str='', line4:str=''):
  oled.fill(0)
  oled.text(line1, 2, 2)
  oled.text(line2, 2, 17)
  oled.text(line3, 2, 32)
  oled.text(line4, 2, 47)
  oled.show()

displayView(
  'Hello, Urish!', 
  'Hello, Milo!', 
  'Hello, Alek!')



outAddPin = Pin(2, Pin.OUT)  
inAddPin = Pin(15, Pin.IN) # D15 Pin: detect the button clicking
outAddPin.value(1) 

outSubPin = Pin(12, Pin.OUT)  
inSubPin = Pin(13, Pin.IN) # D13 Pin: detect the button clicking
outSubPin.value(1) 


# MQTT Server Parameters
MQTT_CLIENT_ID = "my_pico_mqtt_client"
MQTT_BROKER    = "broker.emqx.io"
MQTT_USER      = ""
MQTT_PASSWORD  = ""
MQTT_TOPIC     = "MiloTopic"

print("Connecting to WiFi", end="")
displayView(
  'Connecting to', 
  'Wifi ... ', 
  '')

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Wokwi-GUEST', '')
while not sta_if.isconnected():
  print(".", end="")
  time.sleep(0.1)
print(" Connected!")
displayView(
  'Wifi Connected', 
  '', 
  '')
print("Connecting to MQTT server... ", end="")
displayView(
  'Wifi Connected.', 
  'Connecting to ', 
  'MQTT Server...')

client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD)
client.connect()

print("Connected!")
displayView(
  'Wifi Connected.', 
  'MQTT Connected. ', 
  'Start to click ',
  'button to count')
while True:
  if inAddPin.value() == 1:
    print("MQTT Add")
    client.publish(MQTT_TOPIC, "add")
    displayView( 
      'MQTT Connected. ', 
      'Start to click ',
      'button to count',
      'MQTT pub ++1 '
      )

  elif inSubPin.value() == 1:
    print("MQTT Sub")
    client.publish(MQTT_TOPIC, "sub")
    displayView( 
      'MQTT Connected. ', 
      'Start to click ',
      'button to count',
      'MQTT pub --1 '
      )

  time.sleep(1)
