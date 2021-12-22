from model import Award, AwardReviewStatus, AwardType, PermissionType, Subject, SubjectType, Grade, User, UserState, Permission
from user import _verify_token


def _has_student_full_permission_rw(user, student_uid):
    try:
        student = User.get_by_id(student_uid)
        if user.state == UserState.sysadmin:
            return True
        if user.state == UserState.operator:
            return Permission.get(Permission.uid == user.uid, Permission.class_id == student.class_id_id) == PermissionType.readwrite
    except (User.DoesNotExist, Permission.DoesNotExist):
        return False

    return False


def _has_student_full_permission_r(user, student_uid):
    try:
        student = User.get_by_id(student_uid)
        if user.state == UserState.sysadmin:
            return True
        if user.state == UserState.operator:
            return Permission.get(Permission.uid == user.uid, Permission.class_id == student.class_id_id) >= PermissionType.readonly
    except (User.DoesNotExist, Permission.DoesNotExist):
        return False

    return user.uid == student_uid


def student_grade_add_update(token, student_uid, grade_list):
    uid = _verify_token(token)
    user = User.get_by_id(uid)
    if not _has_student_full_permission_rw(user, student_uid):
        raise ValueError("permission denied")

    for item in grade_list:
        subject_id = Subject.get_or_none(Subject.name == item.subject_name)
        if not subject_id:
            subject_id = Subject.create(type=SubjectType.unknown, name=item.subject_name).subject_id

        grade = Grade.get_or_none(Grade.uid == student_uid, Grade.subject_id == subject_id)
        if grade:
            grade.score = item.score
        else:
            Grade.create(subject_id=subject_id, score=item.score)

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


def student_award_list(token, student_uid):
    uid = _verify_token(token)
    user = User.get_by_id(uid)
    if not _has_student_full_permission_r(user, student_uid):
        raise ValueError("permission denied")

    query = Award.select().where(Award.uid == student_uid)
    data = [{
        "award_id": x.award_id,
        "type": x.type,
        "level": x.level,
        "name": x.name,
        "note": x.note,
        "review_status": x.review_status,
        "review_note": x.review_note,
        "date": x.date
    } for x in query]
    return {"status": "ok", "award_list": data}


def student_award_add(token, student_uid, type, level, name, note, date):
    uid = _verify_token(token)
    user = User.get_by_id(uid)
    if not _has_student_full_permission_rw(user, student_uid):
        raise ValueError("permission denied")

    if Award.get_or_none(Award.uid == student_uid, Award.name == name):
        raise ValueError("award exist")

    # TODO: verify type
    Award.create(uid=student_uid, type=type, level=level, name=name, note=note, date=date, review_status=AwardReviewStatus.pending)

    return {"status": "ok"}


def student_award_update(token, student_uid, award_id, award_update):
    uid = _verify_token(token)
    user = User.get_by_id(uid)

    award = Award.get_or_none(Award.award_id == award_id)
    if not award:
        raise ValueError("permission denied")

    if student_uid != award.uid_id:
        raise ValueError("permission denied")

    if not _has_student_full_permission_rw(user, student_uid):
        raise ValueError("permission denied")

    # TODO: verify name(if duplicate), type, review_status

    if _has_student_full_permission_rw(user, student_uid):
        for k, v in award_update:
            if v is not None:
                setattr(award, k, v)
        award.save()

    # TODO: is_student_self = uid == student_uid

    else:
        raise ValueError("permission denied")

    return {"status": "ok"}

def student_advise(token, student_uid):
    uid = _verify_token(token)
    user = User.get_by_id(uid)
    if not _has_student_full_permission_r(user, student_uid):
        raise ValueError("permission denied")

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
