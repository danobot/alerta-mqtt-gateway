import json
import logging
from listener import Listener

class JsonListener(Listener):
  def __init__(self, topic, config):
    super().__init__(topic, config)
    self.listeners = self.config.get("listeners", [])
    # logging.info("Listeners: " + str(self.listeners))


  def find_listeners(self, topic, payload):
    # logging.info("JsonListener - find_listeners :: START " + str(payload))
    j = json.loads(payload)

    matches = []
    for l in self.listeners:
      payloadValue = j[self.config["attribute"]] 
      if l.get('value') == payloadValue:
        # logging.info("Listener matches - %s" % (l))
        matches.append(l)
    return matches
