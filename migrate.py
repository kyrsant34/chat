from app.base.models import BaseModel
from app.auth.models import *
from app.chat.models import *

db.set_allow_sync(True)
for cls in BaseModel.__subclasses__():
    print(f'migrate: {cls.__name__}')
    cls.create_table(True)
