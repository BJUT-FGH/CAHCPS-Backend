from model import PermissionType, User, UserState, Permission
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


def student_advise(token, student_uid):
    uid = _verify_token(token)
    user = User.get_by_id(uid)
    if not _has_student_full_permission_r(user, student_uid):
        raise ValueError("permission denied")

    # TODO: this is only a example
    from utils import scores
    w, w_msg = scores.wisdom_score(85, "无", 0, grade=1)
    m, m_msg = scores.moral_score(5, grade=1)
    p, p_msg = scores.physical_score(96, 1, grade=1)
    a, a_msg = scores.aesthetic_score(2, grade=1)
    l, l_msg = scores.labor_score(is_union_worker=True, is_meida_worker=False, is_class_worker=False, grade=1)

    from utils.comments import composite_comments
    return {
        "status": "ok",
        "advise": {
            "wisdom": {"score": w, "msg": w_msg},
            "moral": {"score": m, "msg": m_msg},
            "physical": {"score": p, "msg": p_msg},
            "aesthetic": {"score": a, "msg": a_msg},
            "labor": {"score": l, "msg": l_msg},
        },
        "sum_up": composite_comments(student_uid)
    }

