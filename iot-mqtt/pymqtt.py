import paho.mqtt.client as mqtt
import requests

# Setup MQTT broker connection
broker_address = "broker.emqx.io"
port = 1883  # MQTT broker default port
mytopic = "MiloTopic"
# callback of cconnect status
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connect to MQTT broker done")
        # subscribge the topic
        client.subscribe(mytopic)  # the topic your want to subscribe
    else:
        print("connect MQTT broker failed")

# receive the message from on_message callback
def on_message(client, userdata, msg):
    text_message = msg.payload.decode('utf-8')
    print(f"Subscribed Topic '{msg.topic}' Message：{text_message}")
    # filter the message 'add' to count up for reflex webapp and 'sub' to count donw for reflex webapp
    sub_url = "http://localhost:8000/sub_state_count/"
    add_url = "http://localhost:8000/add_state_count/"
    request_url = ""
    if text_message=="add":
        request_url = add_url
    elif text_message=="sub":
        request_url = sub_url
    if request_url != "":
        try:
            response = requests.get(request_url)
            # check the http response
            if response.status_code == 200:
                print(f"Success to request. And the responsed content is {response.text}")
            else:
                print(f"Request failed,  HTTP Stuats code:{response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Http Reqeust Failed: {e}")


# create MQTT client instance
client = mqtt.Client()

# setup callback for the connection and the message
client.on_connect = on_connect
client.on_message = on_message

# Connect to  MQTT broker
client.connect(broker_address, port, keepalive=60)

# Start MQTT client
client.loop_start()

# publish one message for test
client.publish(mytopic, "This is a test message")  

# Keep running
try:
    while True:
        pass
except KeyboardInterrupt:
    # to disconnect 
    client.disconnect()
    client.loop_stop()
