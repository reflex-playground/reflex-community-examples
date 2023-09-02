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