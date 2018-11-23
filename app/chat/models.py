import datetime

import peewee

from app.auth.models import User
from app.base.models import BaseModel
from app.settings import db


class Chat(BaseModel):
    creator = peewee.ForeignKeyField(User, null=True)#, backref='chats')
    created_at = peewee.DateTimeField(default=datetime.datetime.now)


class Message(BaseModel):
    text = peewee.TextField()
    user = peewee.ForeignKeyField(User)
    chat = peewee.ForeignKeyField(Chat)
    created_at = peewee.DateTimeField(default=datetime.datetime.now, index=True)
    is_published = peewee.BooleanField(default=True)

    async def save(self, user, msg, **kw):
        result = await self.collection.insert({'user': user, 'msg': msg, 'time': datetime.now()})
        return result

    async def get_messages(self):
        messages = self.collection.find().sort([('time', 1)])
        return await messages.to_list(length=None)


class UserToChat(BaseModel):
    user = peewee.ForeignKeyField(User)
    chat = peewee.ForeignKeyField(Chat)

    # class Meta(BaseModel.Meta):
    class Meta:
        database = db
        primary_key = peewee.CompositeKey('user', 'chat')
