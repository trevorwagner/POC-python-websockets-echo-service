# WebSocket Echo Service

This codebase provides a very basic demonstration of how to wire up a WebSocket
server (powered by [websockets](https://websockets.readthedocs.io/en/stable/)) 
to a backend service that uses a pub/ sub pattern to transmit new messages to/ 
from a handler class responsible for processing the echos.

What this essentially demonstrates is three things:

1. Messages route to/ from the Echo handler as expected.
2. The service starts/ stops gracefully.
3. Both `host` and `port` can be configured as needed (see **Configuring** 
below).


## Running

Run locally:

```sh
pip install -r requirements.txt
python3 ./main.py
```

The echo service will return any message passed to it.

For referece, this has been tested primarily with a client also built from the 
`websockets` package. Other clients will likely need to manage client pinging/ 
heartbeat manually, which `websockets` does under the hood.

Run in Docker contianer:

```sh
bash ./util/build_container.sh
bash ./util/run_container.sh
```

## Interaction
TBD

## Configuring

`main.py` accepts two arguments, passed as follows:

- `--host=` describes the hostname the WebSocket server is expected to bind to.
- `--port=` describes the number the WebSocket server is expected to serve on.