# WSWebcam

A WSWebcam é uma biblioteca para facilitar streaming de dispostivos de video via rede utilizando o protocolo websocket.

Sua arquitetura é baseada no modelo cliente/servidor. Onde o Dispotivo serial é o servidor e qualquer cliente que conheca seu endereço e porta pode se comunicar com ele.

## Uso/Exemplos
```python
# python -m wswebcam -h
usage: __main__.py [-h] [-c] [-s] [-p PORT] [-a ADDRESS] [-d DEVICE] [-v] [-g]

wswebcam - Websocket to WebcamBridge

options:
  -h, --help            show this help message and exit
  -c, --client          Run as a client
  -s, --server          Run as a server
  -p PORT, --port PORT  Port to listen on
  -a ADDRESS, --address ADDRESS
                        Address to connect to (default: localhost)
  -d DEVICE, --device DEVICE
                        Serial device to connect to (default: 0)
  -v, --verbose         Enable verbose logging
  -g, --gui             Run GUI to view the frame
```

#### Server - [Cmdlt, Instance and Context Manager]
```bash
 # Start a server at 8050 with command line
 python -m wswebcam -s -p 8050
```
```python
# Server as Instance
from wswebcam.server import Server
import asyncio

async def main():
    await Server("0.0.0.0", 8050, 0).run()

asyncio.run(main())
```
```python
# Server as context manager]
from wswebcam.server import Server
import asyncio

async def main():
    async with Server("0.0.0.0", 8050, 0) as server:
        await asyncio.sleep(10)

asyncio.run(main())
```
#### Client - [Cmdlt, Instance and Context Manager]
```bash
 # Connect a client on server at 0.0.0.0:8050
 python -m wswebcam -c -a 0.0.0.0 -p 8050 
```
```python
# Client as Instance
from wswebcam.client import Device as Client
from wswebcam.protocol import package
import asyncio

async def main():
    await client = Client("ws://0.0.0.0:8050")
    await client.connect()
    await client.read()
    await client.disconnect()

asyncio.run(main())
```
```python
# Client as context manager
from wswebcam.client import Camera as Client
import asyncio

async def main():
    async with Client("ws://0.0.0.0:8050") as client:
        await client.read()
```