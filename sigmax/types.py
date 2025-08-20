from typing import *
from pydantic import BaseModel


class User(BaseModel):
    base_url: str
    base_raw_url: str

    name: str
    first_name: str | None
    last_name: str | None
    description: str

    phone: int
    options: list[str]
    photo_id: int | None
    id: int


    @classmethod
    def from_payload(cls, payload: dict) -> "User":
        cls.base_url: str = payload['baseUrl']
        cls.base_raw_url: str = payload['baseRawUrl']
        
        cls.name: str = payload['names'][0].get('name')
        cls.first_name: str | None = payload['names'][0].get('firstName')
        cls.last_name: str | None = payload['names'][0].get('lastName')
        cls.description: str = payload['description']

        cls.phone: int | None = payload.get('phone')
        cls.options: list[str] = payload['options']
        cls.photo_id: int | None = payload['photoId']
        cls.id: int = payload['id']

        return cls


class UserInfo(BaseModel):
    id: int
    user: User
    

    @classmethod
    def from_payload(cls, payload: dict) -> "UserInfo":
        cls.user: User = User.from_payload(payload['profile'])
        cls.id = cls.user.id

        return cls


class Message(BaseModel):
    chat_id: int # Chat ID where the message was sent
    id: int # ID of the message
    sender_id: int | None # ID of who sent the message
    timestamp: int # Timestamp when the message was sent
    text: str # Text of the message
    cid: int | None # Message CID
    attaches: list # List of attachments
    chat: "Chat | None" # Chat where the message was sent


    @classmethod
    def from_payload(cls, payload: dict) -> "Message":
        if not payload.get('message'): 
            data = {'message': payload}
            return Message.from_payload(data)

        cls.chat_id: int = payload.get('chatId')
        cls.id: int = payload['message']['id']
        cls.sender_id: int | None = payload['message'].get('sender')
        cls.timestamp: int = payload['message']['time']
        cls.text: str = payload['message']['text']

        cls.attaches: list = payload['message']['attaches']
        cls.cid: int | None = payload['message'].get('cid')

        cls.chat = Chat.from_payload(payload['chat']) if payload.get('chat') else None

        return cls
    

class ChatOptions(BaseModel):
    sign_admin: bool
    official: bool
    only_owner_can_change_icon_title: bool
    only_admin_can_add_member: bool
    only_admin_can_call: bool
    sent_by_phone: bool
    all_can_pin_message: bool


    @classmethod
    def from_payload(cls, payload: dict) -> "ChatOptions":
        payload = {i.lower(): v for i, v in payload.items()}
        try:
            data = cls.model_validate(payload)
        except:
            return None
        return data


class Chat(BaseModel):
    raw: dict # Raw data received from API
    id: int # Chat ID
    cid: int # CID
    status: Literal['ACTIVE', 'REMOVED', 'LEFT', 'CLOSED'] # User status in the chat
    type: Literal['CHAT', 'DIALOG', 'CHANNEL'] # Chat type (DM or group)
    base_raw_icon_url: str | None # Raw Icon URL
    base_icon_url: str | None # Icon URL
    link: str | None # Link to chat
    participants_count: int | None # Number of participants
    options: ChatOptions | None # Chat permissions
    title: str | None # Chat title
    description: str | None # Chat description
    owner: int # Chat owner ID
    join_time: int # When the user joined the chat
    created: int # When the chat was created
    new_messages: int # Number of new messages
    last_mesage: Message | None # Last message sent in chat
    participants: dict[int, int] # Dict of participants and their last seen times


    @classmethod
    def from_payload(cls, payload: dict) -> "Chat":
        cls.raw = payload
        cls.id = payload['id']
        cls.cid = payload.get('cid')
        cls.status = payload['status']
        cls.type = payload['type']
        cls.base_icon_url = payload.get('baseIconUrl')
        cls.base_raw_icon_url = payload.get('baseRawIconUrl')
        cls.link = payload.get('link')
        cls.participants_count = payload.get('participantsCount')
        cls.options = ChatOptions.from_payload(payload['options']) if payload.get('options') else None
        cls.title = payload.get('title')
        cls.description = payload.get('description')
        cls.owner = payload['owner']
        cls.join_time = payload['joinTime']
        cls.created = payload['created']
        cls.new_messages = payload.get('newMessages', 0)
        cls.last_mesage = Message.from_payload(payload['lastMessage']) if payload.get('lastMessage') else None
        cls.participants = payload['participants']

        return cls