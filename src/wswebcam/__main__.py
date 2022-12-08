# Argparser
import argparse
parser = argparse.ArgumentParser(description='wswebcam - Websocket to Serial Bridge')
parser.add_argument('-c', '--client', action='store_true', help='Run as a client')
parser.add_argument('-s', '--server', action='store_true', help='Run as a server')
parser.add_argument('-p', '--port', type=int, default=8010, help='Port to listen on')
parser.add_argument('-a', '--address', type=str, default='localhost', help='Address to connect to (default: localhost)')
parser.add_argument('-d', '--device', type=str, default='0', help='Serial device to connect to (default: 0)')
parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose logging')
parser.add_argument('-g', '--gui', action='store_true', help='Run GUI to view the frame')
args = parser.parse_args()

# Logging
import logging
import asyncio
logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
log = logging.getLogger(__name__)

# Client
if args.client:
    print('Running as client on', args.address, args.port)
    from .client import main
    asyncio.run(main(f'ws://{args.address}:{args.port}', args.gui))

# Server
elif args.server:
    print('Running as server on', args.address, args.port)
    from .server import main
    asyncio.run(main(args.address, args.port, device=args.device))

def main(*args):
    parser.print_help()
