import asyncio
import websockets
import json

class WebSocketServer:
    def __init__(self, host='localhost', port=8765):
        self.host = host
        self.port = port
        self.clients = set()

    async def register(self, websocket):
        self.clients.add(websocket)

    async def unregister(self, websocket):
        self.clients.remove(websocket)

    async def start_server(self):
        self.server = await websockets.serve(self.handle_messages, self.host, self.port)

    async def handle_messages(self, websocket, path):
        await self.register(websocket)
        try:
            async for message in websocket:
                print(f"Received message: {message}")
                await self.handle_client_message(websocket, message)
        finally:
            await self.unregister(websocket)

    async def handle_client_message(self, websocket, message):
        # Here you can decide how to handle messages and to which client(s) to send responses
        response = json.dumps({"response": "Message received"})
        await websocket.send(response)  # Sending response back to the sender
        # If you want to send a message to a specific client, you can use their websocket object.

    async def send_to_client(self, client_websocket, message):
        # Send a message to a specific client
        if client_websocket in self.clients:
            await client_websocket.send(message)

    def run(self):
        asyncio.run(self.start_server())

    def stop(self):
        pass  # Implement graceful shutdown logic if needed

# Usage
server = WebSocketServer()
server.run()
