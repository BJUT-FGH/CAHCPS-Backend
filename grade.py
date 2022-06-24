from model import Subject, SubjectType, Grade, User
from student import _has_student_full_permission_r, _has_student_full_permission_rw
from user import _verify_token

def student_grade_add_update(token, student_uid, grade_list):
    uid = _verify_token(token)
    user = User.get_by_id(uid)
    if not _has_student_full_permission_rw(user, student_uid):
        raise ValueError("permission denied")

    for item in grade_list:
        subject_id = Subject.get_or_none(Subject.name == item.subject_name)
        if not subject_id:
            subject_id = Subject.create(type=item.subject_type, name=item.subject_name, credit=item.subject_credit).subject_id

        grade = Grade.get_or_none(Grade.uid == student_uid, Grade.subject_id == subject_id)
        if grade:
            grade.score = item.score
            grade.save()
        else:
            Grade.create(uid=student_uid, subject_id=subject_id, score=item.score)

    return {"status": "ok"}


def student_grade_list(token, student_uid):
    uid = _verify_token(token)
    user = User.get_by_id(uid)
    if not _has_student_full_permission_r(user, student_uid):
        raise ValueError("permission denied")

    query = Grade.select().where(Grade.uid == student_uid)
    data = [{
        "subject_name": x.subject_id.name,
        "type": x.subject_id.type,
        "credit": x.subject_id.credit,
        "score": x.score
    } for x in query]
    return {"status": "ok", "grade_list": data}
