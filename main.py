import functools
from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, Query, Request

import env
env.load_config()

import user

# Wrapper to return error message when ValueError
def _std_error_handler(func):
    @functools.wraps(func)
    async def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return {"status": "error", "error_msg": str(e)}
    return inner


# FastAPI Route defines begin
app = FastAPI()


# Homepage
@app.get("/")
@_std_error_handler
def welcome():
    raise ValueError("welcome to College-wide Academic and Honors Cyber Profile System (CAHCPS) backend API endpoint, API access only")


# User Register
class User(BaseModel):
    email: str = Query(..., regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    password: str = Query(..., min_length=3)

class UserRegister(User):
    username: str = Query(..., regex=r"^[0-9a-zA-Z_]{3,64}$")

@app.post("/user/register")
@_std_error_handler
def user_register(reg: UserRegister):
    return user.register(reg.email, reg.password, reg.username)


# User Login
@app.post("/user/login")
@_std_error_handler
def user_login(login: User):
    return user.login(login.email, login.password)

