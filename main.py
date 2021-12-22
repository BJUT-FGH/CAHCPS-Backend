import functools
import sys
import traceback
from typing import List, Optional
from pydantic import BaseModel
from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware

import env
env.load_config()

import user
import admin
import grade

# Wrapper to return error message when ValueError
def _std_error_handler(func):
    @functools.wraps(func)
    async def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            tb = sys.exc_info()[-1]
            stk = traceback.extract_tb(tb)
            fname = stk[-1][2] + '(): '
            return {"status": "error", "error_msg": fname+str(e)}
    return inner


student_id_t = Query(..., regex=r"^\d{8}$")
password_t = Query(..., min_length=3)
email_t = Query(..., regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
name_t = Query(..., regex=r"^[\u4e00-\u9fa5]{2,8}$")
email_or_student_id_t = Query(..., regex=r"^\d{8}$|^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

# FastAPI Route defines begin
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


# - Upload Student Grade (add/update)
class StudentGradeUploadReq(BaseModel):
    class Item(BaseModel):
        subject_name: str = Query(..., min_length=2, max_length=100)
        subject_type: int = 0
        score: float
    grade_list: List[Item]

@app.post("/student/{student_id}/grades")
@_std_error_handler
def _(token: str, student_id: int, p: StudentGradeUploadReq):
    return grade.student_grade_add_update(token, student_id, p.grade_list)


# - List Student Grade
@app.get("/student/{student_id}/grades")
@_std_error_handler
def _(token: str, student_id: int):
    return grade.student_grade_list(token, student_id)


# - List Student Award
@app.get("/student/{student_id}/awards")
@_std_error_handler
def _(token: str, student_id: int):
    return grade.student_award_list(token, student_id)


# - Add Student Awards (student/admin)
class StudentAddAwardReq(BaseModel):
    type: int
    level: int = Query(..., ge=1, le=3)
    name: str = Query(..., min_length=2, max_length=100)
    note: str = Query("", max_length=1000)
    date: int

@app.post("/student/{student_id}/awards")
@_std_error_handler
def _(token: str, student_id: int, award: StudentAddAwardReq):
    return grade.student_award_add(token, student_id, award.type, award.level, award.name, award.note, award.date)


# - Update Student Awards (student/admin)
class StudentUpdateAwardReq(BaseModel):
    type: int = None
    level: int = Query(None, ge=1, le=3)
    name: str = Query(None, min_length=2, max_length=100)
    note: str = Query(None, max_length=1000)
    date: int = None
    review_status: int = None
    review_note: str = Query(None, max_length=1000)

@app.put("/student/{student_id}/award/{award_id}")
@_std_error_handler
def _(token: str, student_id: int, award_id: int, award_update: StudentUpdateAwardReq):
    return grade.student_award_update(token, student_id, award_id, award_update)


# - Get Student Advise (snake.ai)
@app.get("/student/{student_id}/advise")
@_std_error_handler
def _(token: str, student_id: int):
    return grade.student_advise(token, student_id)
