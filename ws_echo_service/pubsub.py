import asyncio

__all__ = [
    "Publisher",
    "Subscriber",
]


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

    def clear(cls):
        try:
            del cls._instances[cls]
        except KeyError:
            pass


class Subscriber:
    """Simple subscriber class with a message queue. Publisher can publish as
    many messages as it wants, and `receive()` will return one, FIFO."""

    def __init__(self, name: str):
        self.name = name
        self.messages = []

    async def receive(self):
        while len(self.messages) < 1:
            s = asyncio.ensure_future(asyncio.sleep(0.01))
            try:
                await s
            except asyncio.CancelledError:
                s.cancel()
                await s
                break

        if len(self.messages) > 0:
            return self.messages.pop(0)


class Publisher(metaclass=SingletonMeta):
    """An Observer class (implemented as a Singleton) that serves as an events
    bus for the entire project. Everything sends events to/ gets them from
    subscriptions to Publisher."""

    def __init__(self):
        self.subscribers = {}

    def subscribe(self, subscriber: Subscriber, topic: str):
        """Allows a subscriber to subscribe to a specific topic."""
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(subscriber)
        return

    def unsubscribe(self, subscriber: Subscriber, topic: str):
        if subscriber not in self.subscribers[topic]:
            raise IndexError(
                f"Requested subscriber {subscriber.name} not subscribed to the provided topic {topic}"
            )
        self.subscribers[topic].remove(subscriber)
        return

    def publish(self, message, topic: str):
        if topic in self.subscribers:
            for subscriber in self.subscribers[topic]:
                subscriber.messages.append(message)
        return
