import paho.mqtt.client as mqtt

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
    print(f"Subscribed Topic '{msg.topic}' Message：{msg.payload.decode('utf-8')}")

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
