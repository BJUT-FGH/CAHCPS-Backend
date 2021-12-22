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
    unknown = 0         # 未知
    校选修课 = 8
    实践环节选修课 = 14
    公共基础必修课 = 15
    公共基础选修课_体育 = 1015
    学科基础必修课 = 16
    学科基础选修课 = 17
    专业限选课 = 18
    专业任选课 = 19
    实践环节必修课 = 20
    创新实践环节 = 21
    通识教育选修课 = 22
    自主课程 = 26
    专业选修课 = 27
    体测成绩 = -1
    other = -999


class AwardType(IntEnum):
    unknown = 0
    院级 = 1
    校级 = 2
    # 区级 = 3
    # 市级 = 4
    省级 = 5
    国家级 = 6
    国际级 = 7


class AwardReviewStatus(IntEnum):
    pending = 0
    passed = 1
    reject = 2


# Tables
class Class(_BaseModel):
    class_id = AutoField()
    name = CharField(unique=True)
    note = TextField(default="")


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


class Award(_BaseModel):
    award_id = AutoField()
    uid = ForeignKeyField(User, on_delete='CASCADE')
    type = IntegerField()
    level = IntegerField()
    name = CharField()
    note = TextField(default="")
    review_status = IntegerField()
    review_note = TextField(default="")
    date = DateField()


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
