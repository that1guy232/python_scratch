import asyncio
import threading
from webSocketServer import WebSocketServer
from window import ServerWindow as Window

def start_asyncio_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_forever()

if __name__ == "__main__":
    # Start the asyncio loop in a new thread
    loop_thread = threading.Thread(target=start_asyncio_loop, daemon=True)
    loop_thread.start()

    # Create a new event loop in the main thread (this loop is not running)
    new_loop = asyncio.new_event_loop()

    # Initialize the web server
    ws_server = WebSocketServer()

    # Schedule the server to start in the asyncio loop
    asyncio.run_coroutine_threadsafe(ws_server.start_server(), new_loop)

    # Start the pygame window
    window = Window(800, 600, ws_server)
    window.start()
