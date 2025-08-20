
# More asterisks (*) == Not sure about meaning

POST_USER_AGENT = 6 # Posts the user agent to the API, required to login
POST_TOKEN = 19 # Posts a token / logs in user
GET_NEW_STICKER_SETS = 26 # * Returns list of IDs of recommended sticker sets, paginated
SYNC_REACTION_DATA = 27 # Syncs reaction, sticker pack, favorite stickers data
GET_REACTION_MEDIA = 28 # Can return list of sticker, animoji, sticker set data by IDs
GET_CONTACTS = 32 # Fetch users by their IDs
GET_PRESENCE = 35 # Fetch users' last seen time by their IDs
GET_USER_BY_PHONE = 46 # Fetches a user by their phone number
GET_CHATS_BY_ID = 48 # Fetches chats by their IDs
GET_PREVIEW_MESSAGES = 49 # * Fetches recent messages in a chat
POST_CHAT_ACTION = 50 # * Post an action in a chat (like read messages)
GET_CHATS = 53 # Continuously fetch chats
SEND_MESSAGE = 64 # Post a message in a chat
POST_TYPING = 65 # Post a typing / sending media indicator for a chat
DELETE_MESSAGE = 66 # Delete an existing message for yourself or for the whole chat 
EDIT_MESSAGE = 67 # Edit an existing message
GET_MESSAGES = 71 # Fetch messages from a chat by their IDs
GET_PHOTO_UPLOAD_URL = 80 # Get a URL to upload a photo to
SUBSCRIBE_TO_CHAT = 75 # *** Has a "subscribe" boolean and a chat ID. API returns null
                       # API seems to send new messages regardless of whether the chat is subscribed or not though
SEND_BUTTON_PRESS = 118 # Send a button press to a bot
RECEIVE_MESSAGE = 128 # API sends this to client when a new message is sent or edited
                      # * Client also can send this but idk what for
RECEIVE_CHAT_ACTION = 129 # API sends this to client when someone starts typing or sending something in chat
RECEIVE_READ_STATUS = 130 # * API sends this to client when a user reads a chat to mark messages as read
RECEIVE_USER_JOIN = 132 # API sends this to client when a user joins a chat
RECEIVE_BOT_CALLBACK_POPUP = 143 # API sends this to client when a bot sends a button press callback popup
GET_REFRESH_TOKEN = 158 # *** Zero clue. Returns a short token and refresh timestamp
GET_MESSAGE_REACTONS = 180 # Get a list of reaction for messages by message IDs

# Telemetry

SESSION_ACK = 1 # ***
NAV_EVENT = 5 # ** Posts list of events when switching tabs in app


# Unknown codes
# 177 - You send a chat ID and a "time" (which is 0 in requests), API returns null