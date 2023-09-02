import argparse
import paho.mqtt.publish as publish

# Parse the arguments. 
parser = argparse.ArgumentParser(description='Publish MQTT message')
parser.add_argument('-t', '--topic', required=True, help='MQTT topic')
parser.add_argument('-m', '--message', required=True, help='Message to publish')
args = parser.parse_args()

# MQTT broker 
broker_address = "broker.emqx.io"
port = 1883  # MQTT broker default port

# Publish the message on the topic
try:
    publish.single(args.topic, args.message, hostname=broker_address, port=port)
    print(f"Done to publish the message to the topic '{args.topic}': {args.message}")
except Exception as e:
    print(f"failed to publish: {e}")
