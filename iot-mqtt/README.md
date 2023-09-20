# Basic usage
## Install
```bash
pip install -r requirements.txt
```

## run reflex app
```bash
reflex init
reflex run
```

## Run mqtt 
```bash
python pymqtt.py
```
You can open many terminal to run it again and again. 
And you can see how mqtt run here.


```bash
python mqtt_send.py -t "MiloTopic" -m "TestMessage"
```
After you run the pymqtt.py, you can use the above command to publish the TestMessage for it.   
And the pymqtt.py can receive the TestMessage on the topic "MiloTopic". Because pymqtt.py subscribe  
on the topic "MiloTopic" in default.   

## Run mqtt in hardware ESP-32 with python code
Just refer what the directory say in ./wokwi-esp32. 
You can run in the simulator first. 
That's would be nice if you just want to make your ESP32 real hardware to run this example. 


# How to play all Iot-MQTT Collaborative counter application?

**Terminal 1**
```bash
reflex init
reflex run
```
Just run this reflex webapp 

**Terminal 2**
It will convert received mqtt message and decide to add/sub count value by sending   
http request to the api route of reflex webapp. 
```bash 
python pymqtt.py
```
Just run this mqtt application 

**Terminal 3**
If you want to count up, use the following command. 
```bash
python mqtt_send.py -t "MiloTopic" -m "add"
```
If you want to count down, use the following command.
```bash
python mqtt_send.py -t "MiloTopic" -m "sub"
```

# Some new powerful tool 
$ python mqtttui.py 
You can run Text-UI of MQTT for this demo 