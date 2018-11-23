import peewee

from app.settings import db


class BaseModel(peewee.Model):

    class Meta:
        database = db

    @classmethod
    def objects(self):
        return db.objects

    @classmethod
    def create_object(cls, **kwargs):
        async def call_db():
            return await db.objects.create(cls, **kwargs)
        return call_db()

    @classmethod
    def get_object(cls, **kwargs):
        async def call_db():
            return await db.objects.get(cls, **kwargs)
        return call_db()
