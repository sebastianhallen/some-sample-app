import json
import random
import socketserver
from functools import partial
from http.server import BaseHTTPRequestHandler
from workshopapp.tipoftheday import TipOfTheDaySource

class TipOfTheDayServer(object):
    def serve(self):
        raise RuntimeError('Use a proper tip of the day server')

class SocketServerHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def __init__(self, *args, **kwargs) -> None:
        self.tip_source: TipOfTheDaySource = kwargs.pop("tip_source")
        super().__init__(*args, **kwargs)

    def do_GET(self):
        tips = self.tip_source.tips()
        tip = random.choice(tips)

        response = {
            'tipOfTheDay': tip,
        }
        response_content = json.dumps(response).encode("utf-8")
        print(response)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Content-Length', len(response_content))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        self.wfile.write(response_content)
        

class SocketServerTipOfTheDayServer(TipOfTheDayServer):
    def __init__(self, tip_source: TipOfTheDaySource, port: int=8080, listener_address: str='0.0.0.0') -> None:
        handler_class = partial(
            SocketServerHandler,
            tip_source=tip_source,
        )
        self.request_handler = handler_class
        self.port = port
        self.listener_address = listener_address


    def serve(self):
        print(f'starting server on {self.listener_address}:{self.port}')

        httpd = socketserver.TCPServer((self.listener_address, self.port), self.request_handler)
        httpd.serve_forever()
