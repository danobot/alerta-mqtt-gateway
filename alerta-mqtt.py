#!/usr/bin/env python3

import argparse
import yaml
import signal
import sys
import time
import logging
import os
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

from alertaclient.api import Client
from listener_factory import ListenerFactory

DEBUG = os.getenv('DEBUG') if os.getenv('DEBUG') else False
MQTT_HOST = os.getenv('MQTT_HOST') if os.getenv('MQTT_HOST') else "mqtt"
MQTT_USERNAME = os.getenv('MQTT_USERNAME') if os.getenv('MQTT_USERNAME') else None
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD') if os.getenv('MQTT_PASSWORD') else None
TOPIC = os.getenv('TOPIC') if os.getenv('TOPIC') else 'alerta/test'
TEST_TOPIC = os.getenv('TEST_TOPIC') if os.getenv('TEST_TOPIC') else 'test'

# Logging
log_level = logging.DEBUG if DEBUG else logging.ERROR
logging.basicConfig(level=log_level, datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)-15s [%(levelname)s] %(module)s: %(message)s' )
config = yaml.load(open("config.yaml"), Loader=yaml.CLoader)

mqttClient = mqtt.Client()

if MQTT_USERNAME:
  logging.info("Authenticating to MQTT server.")
  mqttClient.username_pw_set(MQTT_USERNAME, password=MQTT_PASSWORD)
  
mqttClient.connect(MQTT_HOST, 1883, 60)

alertaClient = Client()

topics = []
factory = ListenerFactory()
for topic, config in config["topics"].items():
  logging.info("Creating listener: " + str(config))
  topics.append( factory.create(topic, config) )

def on_connect(client, userdata, flags, rc):
    logging.info("Connected to MQTT broker with result code "+str(rc))

    for topic in topics:
      logging.info("Subscribing to %s " % (topic.topic))
      mqttClient.subscribe(topic.topic)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload
    logging.debug("Message on %s : %s" % (topic, payload))

    for m in filter(lambda x: x.topic == topic, topics):
      matches =  m.find_listeners(topic, payload)
      if len(matches) > 0:
        pass
      for match in matches:
        params = m.generate_heartbeat_params(match, topic, payload)
        logging.debug("Sending heartbeat for  - " + str(match))
        try:
          logging.debug("Sending heartbeat - " + str(params))
          alertaClient.heartbeat(**params)
        except Exception as e:
          logging.error(e)

mqttClient.on_connect = on_connect
mqttClient.on_message = on_message

# Argument Parsing
parser = argparse.ArgumentParser()
args = parser.parse_args()

def main_loop():
    while True:
        mqttClient.loop()
        time.sleep(0.1)  # Add a small sleep to reduce CPU usage

def exithandler(signal, frame):
    mqttClient.disconnect()
    sys.exit(0)

signal.signal(signal.SIGINT, exithandler)

if __name__ == "__main__":
    main_loop()
