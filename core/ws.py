import asyncio
import logging

import websockets

logging.basicConfig(level=logging.INFO)


class PaymentWebSocketClient:
    def __init__(self, uri):
        self.uri = uri
        self.connection = None
        self.reconnect_delay = 5

    async def connect(self):
        while True:
            try:
                logging.info(f"Attempting to connect to {self.uri}")
                self.connection = await websockets.connect(self.uri)
                logging.info("Connected to WebSocket server")
                await self.listen()
            except (websockets.ConnectionClosedError, ConnectionError) as e:
                logging.error(f"Connection error: {e}")
                await asyncio.sleep(self.reconnect_delay)

    async def listen(self):
        async for message in self.connection:
            logging.info(f"Received message: {message}")
            await self.handle_message(message)

    async def handle_message(self, message):
        logging.info(f"Handling message: {message}")

    async def send(self, message):
        if self.connection:
            await self.connection.send(message)
            logging.info(f"Sent message: {message}")

    async def close(self):
        if self.connection:
            await self.connection.close()
            logging.info("WebSocket connection closed")

    def run(self):
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self.connect())
        except KeyboardInterrupt:
            logging.info("Interrupted by user")
        finally:
            loop.run_until_complete(self.close())


async def test_echo():
    uri = 'wss://echo.websocket.org'
    message = 'Test Message'
    async with websockets.connect(uri) as websocket:
        await websocket.send(message)
        response = await websocket.recv()
        print(f"Sent: {message}")
        print(f"Received: {response}")


async def test_websocket_client():
    uri = 'wss://echo.websocket.org'
    async with websockets.connect(uri) as websocket:
        await websocket.send('Test Message')
        response = await websocket.recv()
        print(f"Received: {response}")


if __name__ == "__main__":
    client = PaymentWebSocketClient(uri="wss://echo.websocket.org")
    client.run()

