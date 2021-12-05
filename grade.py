from model import Subject, SubjectType, Grade, User, UserState, Permission
from user import _verify_token

def _has_student_permission_rw(user, student_id):
    student = User.get_by_id(student_id)
    if not student:
        return False

    if user.state == UserState.sysadmin:
        return True
    if user.state == UserState.operator:
        return bool(Permission.get_or_none(Permission.uid == user.uid, Permission.class_id == student.class_id_id))
    return False

def _has_student_permission_r(user, student_id):
    if _has_student_permission_rw(user, student_id):
        return True
    return user.uid == student_id

def student_grade_add_update(token, student_id, grade_list):
    uid = _verify_token(token)
    user = User.get_by_id(uid)
    if not _has_student_permission_rw(user, student_id):
        raise ValueError("student_add(): permission denied")

    for item in grade_list:
        subject_id = Subject.get_or_none(Subject.name == item.subject_name)
        if not subject_id:
            subject_id = Subject.create(type=SubjectType.unknown, name=item.subject_name).subject_id

        grade = Grade.get_or_none(Grade.uid == student_id, Grade.subject_id == subject_id)
        if grade:
            grade.score = item.score
        else:
            Grade.create(subject_id=subject_id, score=item.score)

    return {"status": "ok"}

def student_grade_list(token, student_id):
    uid = _verify_token(token)
    user = User.get_by_id(uid)
    if not _has_student_permission_r(user, student_id):
        raise ValueError("student_add(): permission denied")

    query = Grade.get(Grade.uid == student_id)
    data = [{
        "subject_name": x.subject_id.name,
        "type": x.subject_id.type,
        "credit": x.subject_id.credit,
        "score": x.score
    } for x in query]
    return {"status": "ok", "grade_list": data}

def student_advise(token, student_id):
    uid = _verify_token(token)
    user = User.get_by_id(uid)
    if not _has_student_permission_r(user, student_id):
        raise ValueError("student_add(): permission denied")

    from utils import scores
    w, w_msg = scores.wisdom_score(85, "无", 0, grade=1)
    m, m_msg = scores.moral_score(5, grade=1)
    p, p_msg = scores.physical_score(96, 1, grade=1)
    a, a_msg = scores.aesthetic_score(2, grade=1)
    l, l_msg = scores.labor_score(is_union_worker=True, is_meida_worker=False, is_class_worker=False, grade=1)

    return {
        "status": "ok",
        "advise": {
            "wisdom": {"score": w, "msg": w_msg},
            "moral": {"score": m, "msg": m_msg},
            "physical": {"score": p, "msg": p_msg},
            "aesthetic": {"score": a, "msg": a_msg},
            "labor": {"score": l, "msg": l_msg},
        }
    }
