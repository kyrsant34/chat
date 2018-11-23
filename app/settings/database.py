import os

import peewee_async


DATABASE = {
    'host': os.getenv('DB_HOST', 'db-host'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'qwerty'),
    'database': os.getenv('DB_NAME', 'chat'),
}


db = peewee_async.MySQLDatabase(None)
db.init(**DATABASE)
db.set_allow_sync(False)
db.objects = peewee_async.Manager(db)
