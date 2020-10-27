import json
from listener import Listener

class JsonArrayListener(Listener):
  def __init__(self, topic, config):
    super().__init__(topic, config)

  def match(self, topic, payload):
    j = json.loads(payload)
    heartbeats = self.config.get("heartbeats", [])
    
    return j[self.config["attribute"]] == self.config.get("value")
