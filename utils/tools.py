from model import *


def get_user_name(user_id):
    return User.get_by_id(user_id).name


def _get_subject_id(subject_name):
    return Subject.get(Subject.name == subject_name)


def get_subject_score(user_id, subject_name):
    sid = _get_subject_id(subject_name)
    return Grade.get(Grade.uid == user_id, Grade.subject_id == sid).score


def _get_all_grade_w_weight(user_id):
    grades = Grade.select().where(Grade.uid == user_id)
    return [{
        "score": x.score,
        "credit": x.subject_id.credit,
        "type": x.subject_id.type
    } for x in grades]


def _calc_weighted_average(all_grade):
    all_score = 0
    all_credit = 0
    for g in all_grade:
        if g['type'] == SubjectType.校选修课:
            continue
        all_score += g['score'] * g['credit']
        all_credit += g['credit']
    return all_score / all_credit


def _get_class_user_id(class_id):
    query = User.select().where(User.student_id != "", User.class_id_id == class_id)
    return [{
        "uid": u.uid,
        "name": u.name,
    } for u in query]


def _get_all_weighted_average_score(class_user_id):
    class_weighted_average_score_list = []
    for user in class_user_id:
        user_all_grade = _get_all_grade_w_weight(user.uid)
        user_weighted_average_score = _calc_weighted_average(user_all_grade)
        class_weighted_average_score_list.append(user_weighted_average_score)
    return class_weighted_average_score_list


def get_rank_from_class(user_id):
    class_id = User.select().where(User.uid == user_id)
    class_user_id = _get_class_user_id(class_id)
    class_weighted_average_score_list = _get_all_weighted_average_score(class_user_id)
    class_weighted_average_score_list.sort(reverse=True)
    all_grade = _get_all_grade_w_weight(user_id)
    user_weighted_average_score = _calc_weighted_average(all_grade)
    return class_weighted_average_score_list.index(user_weighted_average_score)


def get_pe_test_score(user_id):
    get_subject_score(user_id, "体测")


def is_has_innovation(user_id):
    query = Award.select().where(Award.uid == user_id)
    return query.count() > 0


def is_has_academic(user_id):
    pass
