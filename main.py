import functools
from typing import List, Optional
from pydantic import BaseModel
from fastapi import FastAPI, Query, Request

import env
env.load_config()

import user
import admin

# Wrapper to return error message when ValueError
def _std_error_handler(func):
    @functools.wraps(func)
    async def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return {"status": "error", "error_msg": str(e)}
    return inner


student_id_t = Query(..., regex=r"^\d{8}$")
password_t = Query(..., min_length=3)
email_t = Query(..., regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
name_t = Query(..., regex=r"^[\u4e00-\u9fa5]{2,8}$")
email_or_student_id_t = Query(..., regex=r"^\d{8}$|^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

# FastAPI Route defines begin
app = FastAPI()


# - Homepage
@app.get("/")
@_std_error_handler
def welcome():
    raise ValueError("welcome to College-wide Academic and Honors Cyber Profile System (CAHCPS) backend API endpoint, API access only")


# - User Login
class UserLoginReq(BaseModel):
    email_or_student_id: str = email_or_student_id_t
    password: str = password_t

@app.put("/user/login")
@_std_error_handler
def _(p: UserLoginReq):
    return user.login(p.email_or_student_id, p.password)


# - User Register (Pre-add student only)
class UserRegisterReq(BaseModel):
    student_id: str = student_id_t
    password: str = password_t
    email: str = email_t
    name: str = name_t

@app.put("/user/register")
@_std_error_handler
def _(p: UserRegisterReq):
    return user.register(p.student_id, p.password, p.email, p.name)


# - User Modify Password
class UserModifyPassword(BaseModel):
    old_password: str = password_t
    new_password: str = password_t

@app.put("/user/password")
@_std_error_handler
def _(token: str, p: UserModifyPassword):
    return user.modify_password(token, p.old_password, p.new_password)


# - Student User Pre-add
class StudentAddReq(BaseModel):
    class_id: int
    class Item(BaseModel):
        student_id: str = student_id_t
        name: str = name_t
    student_list: List[Item]

@app.post("/admin/students")
@_std_error_handler
def _(token: str, p: StudentAddReq):
    return admin.student_add(token, p.class_id, p.student_list)


# - Student List
@app.get("/admin/students")
@_std_error_handler
def _(token: str, class_id: int = None):
    return admin.student_list(token, class_id)


# - Class Add
class ClassAddReq(BaseModel):
    name: str

@app.post("/admin/classes")
@_std_error_handler
def _(token: str, p: ClassAddReq):
    return admin.class_add(token, p.name)

