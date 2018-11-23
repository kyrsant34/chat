import json

from aiohttp_session import get_session
from aiohttp import web, WSMsgType
import aiohttp_jinja2

from app.auth.models import User
from app.settings import logger
from .models import Chat, UserToChat, Message


class ChatList(web.View):

    async def get(self):
        chats = await Chat.objects().execute(Chat.select(Chat.id))
        return web.json_response([chat.id for chat in chats])


class BeginChat(web.View):

    @aiohttp_jinja2.template('chat/chat.html')
    async def post(self):
        data = await self.request.post()
        # no validate sql injection
        chat_id = data.get('chat_id')
        session = await get_session(self.request)
        current_user = await User.get_object(username=session.get('username'))
        # либо создаём связь с существующим чатом
        if chat_id:
            try:
                chat = await Chat.get_object(id=chat_id)
            except Chat.DoesNotExist as exc:
                logger.error(f'{exc}')
                chat = await Chat.create_object(id=chat_id)
            try:
                u2c = await UserToChat.get_object(user=current_user.id, chat=chat.id)
            except UserToChat.DoesNotExist as exc:
                logger.error(f'{exc}')
                with UserToChat.objects().allow_sync():
                    u2c = await UserToChat.create_object(user=current_user.id, chat=chat.id)
        # либо создаём новый чат и добавляем туда текущего юзера + из request.post()['users']
        else:
            chat = await Chat.create_object(creator=current_user.id)
            usernames = data.get('usernames') or []
            if usernames:
                usernames = json.loads(usernames)
            usernames += [current_user.username]
            users = await User.objects().execute(User.select().where(User.username.in_(usernames)))
            with UserToChat.objects().allow_sync():
                for user in users:
                    u2c = await UserToChat.create_object(user=user.id, chat=chat.id)

        return {'router': self.request.app.router, 'chat_id': chat.id, 'current_user': current_user}


class WebSocket(web.View):

    async def get(self):
        chat_id = self.request.match_info.get('chat_id')
        chat = await Chat.get_object(id=chat_id)

        ws = web.WebSocketResponse()
        await ws.prepare(self.request)

        self.request.app.websockets[chat_id] = self.request.app.websockets.get(chat_id, [])
        session = await get_session(self.request)
        curent_user = await User.get_object(username=session.get('username'))

        for _ws in self.request.app.websockets[chat_id]:
            _ws.send_str(f'{curent_user.username} joined')
        self.request.app.websockets[chat_id].append(ws)

        # previous_messages = await Message.objects().execute(Message.select(Message.text).where(Message.chat == int(chat_id)))
        # await ws.send_str('\n'.join(f'{msg.user.username}: {msg.text}' for msg in previous_messages))

        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                if msg.data == 'close':
                    await ws.close()
                else:
                    for _ws in self.request.app.websockets[chat_id]:
                        if _ws != ws:
                            await _ws.send_str(f'{curent_user.username}: {msg.data}')
                    await Message.create_object(text=str(msg.data),
                                                chat=chat.id,
                                                user=curent_user.id)
            elif msg.type == WSMsgType.ERROR:
                logger.info('ws connection closed with exception %s' % ws.exception())

        self.request.app.websockets[chat_id].remove(ws)
        for _ws in self.request.app.websockets[chat_id]:
            _ws.send_str(f'{curent_user.username} disconected')
        if len(self.request.app.websockets[chat_id]) == 0:
            del self.request.app.websockets[chat_id]
        logger.info('websocket connection closed')

        return ws
