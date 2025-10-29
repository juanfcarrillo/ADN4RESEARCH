from collections import defaultdict

class EventBus:
    def __init__(self):
        self.subscribers = defaultdict(list)

    def subscribe(self, event_name, handler):
        self.subscribers[event_name].append(handler)

    def publish(self, event_name, data):
        for handler in self.subscribers[event_name]:
            handler(data)

bus = EventBus()
