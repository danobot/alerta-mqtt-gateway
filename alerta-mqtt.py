# curl -XPOST http://tower.local:8763/api/heartbeat -H 'Authorization: Key a7RtkQqM5PngVpmGnW4vb4hzBVZfBX3RZ6oMZiB8N9XUvJhuCNveNvbC5XvLhPF' -H 'Content-type: application/json' -d '{
#       "origin": "cluster05",
#       "timeout": 120,
#       "tags": ["db05", "dc2"],
#       "attributes": {
#         "environment": "Production",
#         "service": [
#           "Core",
#           "HA"
#         ],
#         "group": "Network",
#         "severity": "major"
#       }
#     }'


import argparse, yaml
import signal
import sys
import time
import logging
import os
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

import alertaclient



ALERTA_ENDPOINT = os.getenv('ALERTA_ENDPOINT') if os.getenv('ALERTA_ENDPOINT') else "tower.local"
ALERTA_PORT = os.getenv('ALERTA_PORT') if os.getenv('ALERTA_PORT') else "8763"
ALERTA_API_KEY = os.getenv('ALERTA_API_KEY')
MQTT_HOST = os.getenv('MQTT_HOST') if os.getenv('MQTT_HOST') else "tower.local"
TOPIC = os.getenv('TOPIC') if os.getenv('TOPIC') else 'alerta/test'
TEST_TOPIC = os.getenv('TEST_TOPIC') if os.getenv('TEST_TOPIC') else 'test'




# Logging
logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)-15s [%(levelname)s] %(module)s: %(message)s' )
config = yaml.load(open("config.yaml"), Loader=yaml.CLoader)

client = mqtt.Client()

client.connect(MQTT_HOST, 1883, 60)

def on_connect(client, userdata, flags, rc):
    logging.info("Connected to MQTT broker with result code "+str(rc))
    logging.info(config["topics"].keys())
    for key in config["topics"].keys():
      logging.info("Subscribing to %s " % (key))
      client.subscribe(key)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    topic = msg.topic

    client = Client()
    client.heartbeat(origin='baz')

    if topic == MQTT_TEST_TOPIC:
        client.publish(TEST_TOPIC  + "/result", payload=msg.payload, qos=0, retain=False)
        return

client.on_connect = on_connect
client.on_message = on_message

# Argument Parsing
parser = argparse.ArgumentParser()
args = parser.parse_args()

def exithandler(signal, frame):
    client.disconnect()
    sys.exit(0)

signal.signal(signal.SIGINT, exithandler)
