from matcher_topic import TopicMatcher
from matcher_json import JsonMatcher

class MatcherFactory:
  def create(self, topic, config):
    if "type" in config:
      
      if config["type"] == "json":
        return JsonMatcher(topic, config)

      if config["type"] == "topic":
        return TopicMatcher(topic, config)
    else:
      return TopicMatcher(topic, config)