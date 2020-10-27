from matcher import Matcher

class TopicMatcher(Matcher):
  def __init__(self, topic, config):
    super().__init__(topic, config)

  def match(self, topic, payload):
    return self.topic == topic

    