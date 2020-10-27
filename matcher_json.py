import json
from matcher import Matcher

class JsonMatcher(Matcher):
  def __init__(self, topic, config):
    super().__init__(topic, config)

  def match(self, topic, payload):
    j = json.loads(payload)
    return j[self.config["attribute"]] == self.config.get("value")
