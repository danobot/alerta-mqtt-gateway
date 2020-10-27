class Matcher:
  def __init__(self, topic, config):
    self.topic = topic
    self.config = config

  def match(self, topic, payload):
    return False
  
  def heartbeat(self, topic, payload ):
    default = {
      'origin': self.config.get("origin", topic),
      'tags': self.config.get("tags",list()),
      'attributes': self.config.get("attributes", dict()),
      'timeout': self.config.get("timeout", 24*3600)
    }
 

    return {**default}