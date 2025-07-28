import asyncio, websockets

from ws_echo_service.echo_handler import EchoHandler
from ws_echo_service.pubsub import Publisher, Subscriber


async def producer(websocket: websockets.ServerConnection, subscriber: Subscriber):
    """Listens for new messages from `InterviewManager`."""

    while True:

        try:
            inbound = asyncio.create_task(subscriber.receive())
            new_message = await inbound
            await websocket.send(new_message)

        except asyncio.CancelledError:
            inbound.cancel()
            await inbound
            break


async def consumer(websocket: websockets.ServerConnection, subscriber: Subscriber):
    """Listens for new messages from WebSocket."""

    while True:

        try:
            message = asyncio.create_task(websocket.recv())
            await message
            Publisher().publish(message.result(), subscriber.name)

        except asyncio.CancelledError:
            message.cancel()
            await message
            break


async def client_handler(client: websockets.ServerConnection):
    """A handler for the consumer/ server to handle client connections."""
    print(f"WebSocket client {client.id} connected.")

    outbound_messages = Subscriber(f"new-interview-messages-{client.id}")
    Publisher().subscribe(outbound_messages, outbound_messages.name)

    inbound_messages = Subscriber(f"new-websocket-messages-{client.id}")
    Publisher().subscribe(inbound_messages, inbound_messages.name)

    echo_handler = asyncio.ensure_future(
        EchoHandler(
            ws_events=inbound_messages, interview_events=outbound_messages
        ).interview_visitor()
    )

    consumer_task = asyncio.ensure_future(consumer(client, inbound_messages))
    producer_task = asyncio.ensure_future(producer(client, outbound_messages))

    tasks = (echo_handler, consumer_task, producer_task)

    runtime = asyncio.gather(*tasks)

    def shutdown():
        Publisher.unsubscribe(outbound_messages, outbound_messages.name)
        Publisher.unsubscribe(inbound_messages, inbound_messages.name)
        for task in tasks:
            task.cancel()

    try:
        await runtime

    except asyncio.CancelledError:
        shutdown()

    except websockets.ConnectionClosedOK:
        print(f"Client {client.id} disconnected gracefully.")
        shutdown()

    except websockets.ConnectionClosedError as e:
        print(f"Client {client.id} disconnected with error: {e}")
        shutdown()


async def main(host: str, port: int):
    async with websockets.asyncio.server.serve(client_handler, host, port) as server:
        print(f"WebSocket server (POC-ws-echo-service) listening on ws://{host}:{port}")
        await server.wait_closed()
