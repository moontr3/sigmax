from typing import *
import asyncio
import json
import time
from websockets.asyncio.client import connect
from .opcodes import *
from .config import *
from .types import *


class Request:
    def __init__(self, data: dict):
        self.data: dict = data
        self.payload: dict = data['payload']
        self.cmd: int = data['cmd']
        self.opcode: int = data['opcode']
        self.seq: int = data['seq']
        self.ver: int = data['ver']


class Client:
    def __init__(self):
        self.websocket = None
        self.seq: int = 0
        self.awaiting_reqs: Dict[int, "Request | None"] = {}
        self.receiving = False

        self.handlers: Dict[str, List[Callable]] = {
            "any": [],
            "start": [],
            "message": []
        }


    async def send_json(self, opcode: int, data: dict, cmd: int = 0):
        '''
        Sends a JSON structure to the API.
        
        :param opcode: Opcode.
        :param data: Data.
        :param cmd: Command status (2 - error).
        '''
        self.seq += 1
        await self.websocket.send(json.dumps({
            "ver": 11,
            "cmd": cmd,
            "seq": self.seq,
            "opcode": opcode,
            "payload": data
        }))


    async def wait_for(self, opcode: int, data: dict, cmd: int = 0, timeout_seconds: int = 10) -> Request:
        '''
        Sends a JSON structure to the API and wait for the answer.
        
        :param opcode: Opcode.
        :param data: Data.
        :param cmd: Command status (2 - error).
        '''
        if self.receiving == False:
            return

        await self.send_json(opcode, data, cmd)
        seq = int(self.seq)
        self.awaiting_reqs[self.seq] = None
        start_time = time.monotonic()

        while True:
            if seq not in self.awaiting_reqs:
                return None

            if self.awaiting_reqs[seq] is not None:
                return self.awaiting_reqs.pop(seq)
            
            if time.monotonic()-start_time > timeout_seconds:
                del self.awaiting_reqs[seq]
                return None

            await asyncio.sleep(REQUEST_WAIT_SLEEP_TIME)


    async def recv_json(self) -> Request:
        '''
        Waits until API sends something through the socket.
        '''
        data = await self.websocket.recv()
        return Request(json.loads(data))
    

    async def handle_request(self, req: Request):
        '''
        Handles the request.
        '''
        # on_any handler
        if req.seq not in self.awaiting_reqs:
            for handler in self.handlers["any"]:
                asyncio.create_task(handler(req))
            
        # on_message handler
        if req.opcode == RECEIVE_MESSAGE:
            message = Message(req.payload)

            for handler in self.handlers["message"]:
                asyncio.create_task(handler(message))


    async def start_receiving_reqs(self):
        '''
        Starts receiving requests from the API.
        '''
        if self.receiving:
            return
        
        self.receiving = True

        while self.receiving:
            req = await self.recv_json()

            asyncio.create_task(self.handle_request(req))

            if req.seq in self.awaiting_reqs:
                self.awaiting_reqs[req.seq] = req


    # decorators
    

    def on_start(self):
        '''
        Decorator for receiving requests.
        '''
        def decorator(func):
            self.handlers["start"].append(func)
            return func
        return decorator
    

    def on_any(self):
        '''
        Decorator for receiving requests.
        '''
        def decorator(func):
            self.handlers["any"].append(func)
            return func
        return decorator
    

    def on_message(self):
        '''
        Decorator for receiving messages.
        '''
        def decorator(func):
            self.handlers["message"].append(func)
            return func
        return decorator
    

    # functions
    

    async def send_message(self,
        chat_id: int,
        text: str,
        reply_to: "int | None" = None,
        notify: bool = True
    ):
        data = {
            "chatId": chat_id,
            "message": {
                "text": text,
                "cid": time.time_ns(),
                "elements": [],
                "attaches": []
            },
            "notify": notify
        }

        if reply_to:
            data["message"]["link"] = {
                "type": "REPLY",
                "messageId": str(reply_to)
            }

        out = await self.wait_for(SEND_MESSAGE, data)
        message = Message(out.payload)
        return message
    

    async def edit_message(self,
        chat_id: int,
        message_id: int,
        text: str
    ):
        data = {
            "chatId": chat_id,
            "messageId": message_id,
            "text": text,
        }

        out = await self.wait_for(EDIT_MESSAGE, data)
        data = out.payload
        data['chatId'] = chat_id
        message = Message(data)
        return message

        
    # logging in


    async def login_with_token(self, token: str):
        '''
        Logs in with token.
        '''
        if self.websocket:
            return
        
        async with connect(API_URL) as websocket:
            self.websocket = websocket

            # Sending Useragent
            await self.send_json(POST_USER_AGENT, {
                "userAgent": {
                    "deviceType": "WEB",
                    "locale": "ru_RU",
                    "osVersion": "Windows",
                    "deviceName": "sigmax",
                    "headerUserAgent": "sigmax",
                    "deviceLocale": "en-US",
                    "appVersion": "4.8.42",
                    "timezone": "Europe/Moscow"
                },
                "deviceId": "24092409-2409-2409-2409-240924092409"
            })
            await self.recv_json()

            # Logging in
            await self.send_json(POST_TOKEN, {
                "interactive": True,
                "token": token,
                "chatsSync": 0,
                "contactsSync": 0,
                "presenceSync": 0,
                "draftsSync": 0,
                "chatsCount": 0
            })
            resp = await self.recv_json()

            for i in self.handlers['start']:
                asyncio.create_task(i())
            await self.start_receiving_reqs()
            