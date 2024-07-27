import logging

from listener import Listener

class TopicListener(Listener):
  def __init__(self, topic, config):
    super().__init__(topic, config)

  def find_listeners(self, topic, payload):
    # logging.info("TopicListener - find_listeners :: START " + str(payload))

    if self.topic == topic:
      return [self.config]
    return list()

    