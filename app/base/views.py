from aiohttp import web
import aiohttp_jinja2
from aiohttp_session import get_session
from app.auth.models import User
from app.chat.models import Chat, UserToChat


class Index(web.View):

    @aiohttp_jinja2.template('index.html')
    async def get(self, **kw):
        users = await User.objects().execute(User.select(User.username))
        chats = await Chat.objects().execute(Chat.select(Chat.id))
        chats_dict = {}
        if chats:
            with UserToChat.objects().allow_sync():
                for chat in chats:
                    u2cts = await UserToChat.objects().execute(UserToChat.select(UserToChat.user).where(UserToChat.chat == chat.id))
                    chats_dict[chat.id] = [u2c.user.username for u2c in u2cts]

        session = await get_session(self.request)
        current_user = await User.get_object(username=session.get('username'))

        return {'router': self.request.app.router,
                'users': users,
                'chats': chats_dict,
                'current_user': current_user,
                }
