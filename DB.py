from peewee import *
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

os.makedirs(DATA_DIR, exist_ok=True)

folder_name = "photo_folder"

db_path = os.path.join(DATA_DIR, "database.db")
path = os.path.join(DATA_DIR, "photo_folder")

db = SqliteDatabase(db_path)


class BaseModel(Model):
    id = AutoField()
    name = CharField()

    class Meta:
        database = db


class User(BaseModel):
    chat_id = BigIntegerField(unique=True)
    flag = BooleanField(default=True)

    class Meta:
        table_name = "users"


class Message(BaseModel):
    text_message = TextField()
    date = DateTimeField(default=datetime.now)
    image_data = CharField(null=True)

    class Meta:
        table_name = "messages"


class Actions(BaseModel):
    text_action = TextField()
    date = DateTimeField(default=datetime.now)
    image_data = CharField(null=True)

    class Meta:
        table_name = "actions"


def init_db():
    db.connect(reuse_if_open=True)
    db.create_tables([User, Message, Actions])



