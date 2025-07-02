from typing import *


class Message:
    def __init__(self, payload: dict):
        self.payload: dict = payload

        self.chat_id: int = payload['chatId']
        self.id: int = payload['message']['id']
        self.sender_id: int = payload['message']['sender']
        self.timestamp: int = payload['message']['time']
        self.text: str = payload['message']['text']

        self.cid: "int | None" = payload['message'].get('cid')
        self.attaches: list = payload['message']['attaches']