from peewee import IntegrityError
from model import Class, User, UserState, Permission
from user import _verify_token

def student_add(token, class_id, student_list):
    uid = _verify_token(token)
    user = User.get_by_id(uid)
    if not (
        user.state == UserState.operator
            and Permission.get_or_none(Permission.uid == uid, Permission.class_id == class_id)
        or user.state == UserState.sysadmin
    ):
        raise ValueError("student_add(): permission denied")

    class_ = Class.get_or_none(Class.class_id == class_id)
    if not class_:
        raise ValueError("student_add(): class_id not found")

    failed = []
    for item in student_list:
        try:
            User.create(student_id=item.student_id, name=item.name, class_id=class_id, state=UserState.unregistered)
        except IntegrityError:
            failed.append(item)

    if failed:
        return {"status": "ok", "error_list": failed}
    else:
        return {"status": "ok"}

def student_list(token, class_id):
    uid = _verify_token(token)
    user = User.get_by_id(uid)
    if class_id:
        if not (
            user.state == UserState.operator
            and Permission.get_or_none(Permission.uid == uid, Permission.class_id == class_id)
            or user.state == UserState.sysadmin
        ):
            raise ValueError("student_add(): permission denied")
        query = User.select().where(User.student_id != "", User.class_id_id == class_id)
    else:
        if user.state != UserState.sysadmin:
            raise ValueError("student_add(): permission denied")
        query = User.select().where(User.student_id != "")

    data = [{
        "name": u.name,
        "student_id": u.student_id,
        "email": u.email,
        "class_id": u.class_id_id,
        "state": u.state
    } for u in query]
    return {"status": "ok", "student_list": data}


def class_add(token, name):
    uid = _verify_token(token)
    user = User.get_by_id(uid)
    if user.state != UserState.sysadmin:
        raise ValueError("class_add(): permission denied")

    if Class.get_or_none(Class.name == name):
        raise ValueError("class_add(): class name already exist")

    class_ = Class.create(name=name)
    return {"status": "ok", "class_id": class_.class_id}
