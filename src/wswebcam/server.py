from .protocol import encode
from .device import Camera
from uuid import uuid4
from os import environ

import websockets
import asyncio

class Server:
    """
    Websocket Server with a camera attached.
        :param host: Host to listen on
        :param port: Port to listen on
        :param device: Device to use
        :param loop: Event loop to use

    """
    def __init__(self, host, port, device, loop=None):
        self._id = uuid4()
        self.host = host
        self.port = port
        self.loop = loop or asyncio.get_event_loop()
        self.server = websockets.serve(self.handler, self.host, int(self.port))
        self.camera = Camera(device)
        self._async_stopped = self.loop.create_future()

    async def __aenter__(self):
        return await self.server.__aenter__()

    async def __aexit__(self, *args):
        return await self.server.__aexit__(*args)

    async def run(self):
        async with self.server:
            await self._async_stopped

    async def handler(self, websocket, path):
        while websocket.open:
            try:
                await websocket.recv()
                await websocket.send(encode(self.camera.read()[1]))
            except websockets.ConnectionClosed:
                pass

async def main( host, port, device):
    """
    Main function to run the server    
    """
    return await Server(host, port, device).run()

if __name__ == '__main__':

    HOST = environ.get("SERVER_HOST", "0.0.0.0")
    PORT = environ.get("SERVER_PORT", 8020)
    DEVICE_ID = environ.get("DEVICE_ID", 0)

    asyncio.run(main(HOST, PORT, DEVICE_ID))