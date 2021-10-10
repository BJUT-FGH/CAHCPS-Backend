import time
from hashlib import sha256

import jwt

from env import config, db
from model import User

def _hash_password(password: str) -> str:
    h = sha256()
    h.update(password.encode('utf-8'))
    return h.hexdigest()

def _login(email: str, password: str) -> int:
    password_hash = _hash_password(config['salt'] + password)
    try:
        user = User.get((User.email == email) & (User.password == password_hash))
    except User.DoesNotExist:
        raise ValueError("_login(): Email or Password incorrect")
    return user.uid

def _verify_token(token: str) -> int: # return UID
    try:
        return jwt.decode(token, config['server_secret'], algorithms="HS256")['uid']
    except jwt.InvalidTokenError:
        raise ValueError("_verify_token(): token error")


def register(email: str, password: str, username: str) -> None:
    if User.get_or_none(User.email == email):
        raise ValueError("register(): Email already exist")
    if User.get_or_none(User.username == username):
        raise ValueError("register(): Username already exist")
    password_hash = _hash_password(config['salt'] + password)
    User.create(email=email, password=password_hash, username=username)

    return {"status": "ok"}

def login(email: str, password: str):
    uid = _login(email, password)
    encoded_jwt = jwt.encode(
        {
            "uid": uid,
            "exp": int(time.time()) + 3600*6
        },
        config['server_secret'], algorithm="HS256"
    )
    return {"status": "ok", "token": encoded_jwt}

