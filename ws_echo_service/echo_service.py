import asyncio

from ws_echo_service.pubsub import Publisher, Subscriber


class EchoService:

    def __init__(self, ws_events: Subscriber, echo_events: Subscriber):
        self.ws_events = ws_events
        self.echo_events = echo_events

    async def interview_visitor(self):
        while True:
            updates = asyncio.create_task(self.interview_state.ws_events.receive())
            try:
                message = await updates
                Publisher().publish(
                    message=message, topic=self.interview_state.interview_events.name
                )
            except asyncio.CancelledError:
                updates.cancel()
                break
        return
