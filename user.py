import time
from hashlib import sha256

import jwt

from env import config, db
from model import User, UserState

def _hash_password(password: str) -> str:
    password = config['salt'] + password
    h = sha256()
    h.update(password.encode('utf-8'))
    return h.hexdigest()

UID = int
def _login(email_or_student_id: str, password: str) -> UID:
    password_hash = _hash_password(password)
    try:
        if '@' in email_or_student_id:
            user = User.get(User.email == email_or_student_id, User.password == password_hash)
        else:
            user = User.get(User.student_id == email_or_student_id, User.password == password_hash)
    except User.DoesNotExist:
        raise ValueError("Email/Student_ID or Password incorrect")
    return user.uid

def _verify_token(token: str) -> UID:
    try:
        return jwt.decode(token, config['server_secret'], algorithms="HS256")['uid']
    except jwt.InvalidTokenError:
        raise ValueError("token error")

def login(email_or_student_id: str, password: str):
    uid = _login(email_or_student_id, password)
    encoded_jwt = jwt.encode(
        {
            "uid": uid,
            "exp": int(time.time()) + 3600*24*30
        },
        config['server_secret'], algorithm="HS256"
    )
    return {"status": "ok", "token": encoded_jwt}

def register(student_id: str, password: str, email: str, name: str):
    try:
        user = User.get(User.student_id == student_id, User.name == name)
    except User.DoesNotExist:
        raise ValueError("Verify failed")
    if user.state != UserState.unregistered:
        raise ValueError("Verify failed")
    if User.get_or_none(User.email == email):
        raise ValueError("Email already exist")
    user.password = _hash_password(password)
    user.email = email
    user.state = UserState.normal
    user.save()
    return {"status": "ok"}

def modify_password(token, old_password, new_password):
    uid = _verify_token(token)
    user = User.get_by_id(uid)
    old_password_hash = _hash_password(old_password)
    if old_password_hash == user.password:
        new_password_hash = _hash_password(new_password)
        user.password = new_password_hash
        user.save()
    else:
        raise ValueError("old password wrong")
    return {"status": "ok"}
