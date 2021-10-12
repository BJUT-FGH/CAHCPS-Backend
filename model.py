from typing import Text
from peewee import *
from enum import IntEnum, unique
from env import db

class _BaseModel(Model):
    class Meta:
        database = db

# Enums
class UserState(IntEnum):
    unregistered = 0    # 未注册（新生）
    normal = 1          # 正常用户
    readonly = 2        # 只读用户（毕业生）
    operator = 10       # 管理员（教师）
    sysadmin = 100      # 系统管理工具人

class PermissionType(IntEnum):
    readonly = 1
    readwrite = 2

# Tables
class Class(_BaseModel):
    class_id = AutoField()
    name = CharField(unique=True)
    note = TextField(null=True)

class User(_BaseModel):
    uid = AutoField()
    email = CharField(unique=True, null=True)
    password = CharField(null=True)
    name = CharField()
    state = IntegerField()
    student_id = CharField(null=True, unique=True)
    class_id = ForeignKeyField(Class, null=True)

class Score(_BaseModel):
    uid = ForeignKeyField(User, on_delete='CASCADE')
    subject = CharField()
    score = FloatField()
    class Meta:
        primary_key = CompositeKey('uid', 'subject')

class Permission(_BaseModel):
    class_id = ForeignKeyField(Class, on_delete='CASCADE')
    uid = ForeignKeyField(User, on_delete="CASCADE")
    permission = IntegerField()
    class Meta:
        primary_key = CompositeKey('class_id', 'uid')
