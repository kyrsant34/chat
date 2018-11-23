from app.chat.views import ChatList, WebSocket, BeginChat
from app.auth.views import Login, Register, LogOut, UserList
from app.base.views import Index
from aiohttp import web

async def handler(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)


routes = [
    ('GET', '/', Index,  'index'),
    ('*', '/register/', Register, 'register'),
    ('*', '/login/', Login, 'login'),
    ('*', '/logout/', LogOut, 'logout'),
    ('GET', '/chats/', ChatList,  'chat-list'),
    ('POST', '/chats/begin/', BeginChat,  'begin-list'),
    ('GET', '/chats/{chat_id}/', WebSocket,  'ws-chat'),
    ('GET', '/users/', UserList,  'user-list'),
]