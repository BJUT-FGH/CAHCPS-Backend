from peewee import *
from enum import IntEnum
from env import db

class _BaseModel(Model):
    class Meta:
        database = db

class User(_BaseModel):
    uid = AutoField()
    email = CharField(unique=True)
    password = CharField()
    username = CharField(unique=True)

