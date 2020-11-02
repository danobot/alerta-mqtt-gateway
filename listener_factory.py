from listener_topic import TopicListener
from listener_json import JsonListener
import logging 
class ListenerFactory:
  def create(self, topic, config):
    if "type" in config:
      if config["type"] == "json":
        return JsonListener(topic, config)

      if config["type"] == "topic":
        return TopicListener(topic, config)
    else:
      return TopicListener(topic, config)