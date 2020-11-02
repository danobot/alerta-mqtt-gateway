import logging

class Listener:
  def __init__(self, topic, config):
    self.topic = topic
    self.config = config

  def find_listeners(self, topic, payload):
    return list()
  
  def generate_heartbeat_params(self,match, topic, payload ):
    default = {
      'origin': self.config.get("origin", topic),
      'tags': self.config.get("tags",list()),
      'attributes': self.config.get("attributes", dict()),
      'timeout': self.config.get("timeout", 24*3600)
    }
    
    logging.info("Default config: " + str(default))
    
    hearbeat_global = self.config.get("heartbeat_global", dict())
    logging.info("hearbeat_global: " + str(hearbeat_global))

    match_config = match.get("heartbeat", dict())
    logging.info("match_config: " + str(match_config))

    final = {**default, **hearbeat_global, **match_config}
    logging.info("final config: " + str(final))
    
    return final