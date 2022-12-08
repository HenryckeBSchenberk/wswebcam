import asyncio
from numpy import uint8, ndarray
import websockets
from .protocol import decode
import cv2

class Camera:
    """
        Open an connection to the websocket server.

        (read): Will read a frame from the server and wait for an answer. Returns a numpy.ndarray only.
    """

    def __init__(self, uri:str, loop= None) -> None:
        self.uri = uri

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, *args):
        await self.disconnect()

    async def disconnect(self):
        await self.websocket.close()

    async def connect(self):
        self.websocket = await websockets.connect(self.uri)

    @property
    def frame(self):
        """
        Returns a numpy.ndarray decoded from the data received from the server.

        cap.data can be used to get the raw data.
        """

        return decode(self.data, dtype=uint8)

    async def read(self):
        """
        Read a frame from the server and wait for an answer.
        """
        await self.websocket.send("read")
        self.data = await self.websocket.recv()
        return self.frame

async def unit_test(show=False):
    """
    unit test for the client
    (show): if True will print the package sent and receive

    Steps:
        1. Connect to the server
        2. Get 10 frames
        3. Check if the frames are valid (can be decoded)
        4. Close the connection
    """
    
    value = False
    show and print('='*20, 'UNIT TEST', '='*20)
    show and print("[Starting] Unit Test - Camera Websocket Client")
    try:
        async with Camera("ws://192.168.1.38:8050") as cap:
            assert cap.websocket.open, "Websocket is not open"
            show and print("Camera-Client open --- OK")

            frames = [await cap.read() for _ in  range(10)]
            assert frames is not None, 'No frames received, check if camera is connected on server'
            show and print('Frames received --- OK' )

            for frame in frames:
                assert isinstance(frame, ndarray), 'Frame is not a numpy array, check encode/decode functions'
            show and print('Frames are numpy arrays --- OK' )

        assert cap.websocket.closed, 'Websocket is not closed, check __aexit__ method'
        show and print('Camera-Client closed --- OK' )
        value = True
    except ConnectionRefusedError:
        show and print("Camera-Client open --- Failed")
    finally:
        show and print("[Finished] Unit Test - Camera Websocket Client")
        show and print('='*51)
        return value

async def main(uri, show=False):
    """
    Connect to the server and get a frame.
    (uri): websocket uri
    (show): Will show the frame in a window (an gui is required).
    """
    async with Camera(uri) as cap:
        try:
            while cap.websocket.open:
                frame = await cap.read()
                if show:
                    cv2.imshow('frame', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                else:
                    print(f"Frame: {frame.shape}")
        except KeyboardInterrupt:
            pass

if __name__ == '__main__':
    asyncio.run(main("ws://0.0.0.0:8020"))
