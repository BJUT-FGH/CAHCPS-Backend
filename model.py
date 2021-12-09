from peewee import *
from enum import IntEnum
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

class SubjectType(IntEnum):
    unknown = 0
    basic = 1
    professional = 2
    public = 3
    pe = 4
    pe_test = 5
    other = 6

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

class Subject(_BaseModel):
    subject_id = AutoField()
    type = IntegerField()
    name = CharField(unique=True)
    credit = FloatField()

class Grade(_BaseModel):
    uid = ForeignKeyField(User, on_delete='CASCADE')
    subject_id = ForeignKeyField(User, on_delete='CASCADE')
    score = FloatField()
    class Meta:
        primary_key = CompositeKey('uid', 'subject_id')

class Permission(_BaseModel):
    class_id = ForeignKeyField(Class, on_delete='CASCADE')
    uid = ForeignKeyField(User, on_delete="CASCADE")
    permission = IntegerField()
    class Meta:
        primary_key = CompositeKey('class_id', 'uid')
