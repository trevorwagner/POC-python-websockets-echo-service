import asyncio, sys, websockets

from ws_echo_service.websocket import main

DEFAULT_HOST = "localhost"
DEFAULT_PORT = 8000


if __name__ == "__main__":
    port = DEFAULT_PORT
    host = DEFAULT_HOST

    try:
        port = [a[7:] for a in sys.argv[1:] if a[:7] == "--port="][0]
    except IndexError:
        pass

    try:
        host = [a[7:] for a in sys.argv[1:] if a[:7] == "--host="][0]
    except IndexError:
        pass

    try:
        asyncio.run(main(host=host, port=port))
    except KeyboardInterrupt:
        print("\nProgram interrupted by user (KeyboardInterrupt caught in main).")
    print("Program finished.")
