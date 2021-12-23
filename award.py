from model import Award, AwardReviewStatus, AwardType, User
from student import _has_student_full_permission_r, _has_student_full_permission_rw
from user import _verify_token

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
