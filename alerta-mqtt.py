#!/usr/bin/env python3


import argparse, yaml
import signal
import sys
import time
import logging
import os
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

from alertaclient.api import Client

from listener_factory import ListenerFactory


# ALERTA_ENDPOINT = os.getenv('ALERTA_ENDPOINT') if os.getenv('ALERTA_ENDPOINT') else "tower.local"
# ALERTA_PORT = os.getenv('ALERTA_PORT') if os.getenv('ALERTA_PORT') else "8763"
# ALERTA_API_KEY = os.getenv('ALERTA_API_KEY')
MQTT_HOST = os.getenv('MQTT_HOST') if os.getenv('MQTT_HOST') else "mqtt"
TOPIC = os.getenv('TOPIC') if os.getenv('TOPIC') else 'alerta/test'
TEST_TOPIC = os.getenv('TEST_TOPIC') if os.getenv('TEST_TOPIC') else 'test'




# Logging
logging.basicConfig(level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)-15s [%(levelname)s] %(module)s: %(message)s' )
config = yaml.load(open("config.yaml"), Loader=yaml.CLoader)

mqttClient = mqtt.Client()

logging.info("Hello")
mqttClient.connect(MQTT_HOST, 1883, 60)

alertaClient = Client()

topics = []
factory = ListenerFactory()
for topic, config in config["topics"].items():
  logging.info( "Creating listener: " + str(config))
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
    logging.info("Message on %s : %s" % (topic, payload))

    for m in filter( lambda x: x.topic == topic, topics):
      matches =  m.find_listeners(topic, payload)
      if len(matches) > 0:
        logging.info("find listeners output: " + str(matches))
      for match in matches:
        params = m.generate_heartbeat_params(match, topic, payload)
        logging.info("Sending heartbeat for  - " + str(match))
        logging.info("Sending heartbeat - " + str(params))
        alertaClient.heartbeat(**params)

mqttClient.on_connect = on_connect
mqttClient.on_message = on_message

# Argument Parsing
parser = argparse.ArgumentParser()
args = parser.parse_args()
while True:
  mqttClient.loop()

def exithandler(signal, frame):
    mqttClient.disconnect()
    sys.exit(0)

signal.signal(signal.SIGINT, exithandler)
