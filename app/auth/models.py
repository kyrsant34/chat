import hashlib

import peewee

from app.base.models import BaseModel
from app.settings import SALT


class User(BaseModel):
    username = peewee.CharField(unique=True)
    password = peewee.CharField(max_length=256)
    is_active = peewee.BooleanField(default=True)

    @classmethod
    def create_object(cls, **kwargs):
        if 'password' in kwargs:
            kwargs['password'] = cls.make_hash(kwargs['password'])
        return super().create_object(**kwargs)

    @classmethod
    def get_object(cls, **kwargs):
        if 'password' in kwargs:
            kwargs['password'] = cls.make_hash(kwargs['password'])
        return super().get_object(**kwargs)

    @classmethod
    def make_hash(cls, text):
        text_hash = hashlib.sha512(f'{text}{SALT}'.encode()).hexdigest()
        return text_hash
