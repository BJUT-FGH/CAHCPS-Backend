from model import *


def get_user_name(user_id):
    return User.get_by_id(user_id).name


def _get_subject_id(subject_name):
    return Subject.get(Subject.name == subject_name)


def get_subject_score(user_id, subject):
    sid = _get_subject_id(subject)
    return Grade.get(Grade.uid == user_id, Grade.subject_id == sid).score


def _get_all_grade_w_weight(user_id):
    grades = Grade.select().where(Grade.uid == user_id)
    return [{
        "score": x.score,
        "credit": x.subject_id.credit
    } for x in grades]


def _calc_weighted_average(all_grade):
    all_score = 0
    all_credit = 0
    for g in all_grade:
        all_score += g['score']
        all_credit += g['credit']
    return all_score / all_credit


def get_rank_from_class(user_id):

    pass


def get_pe_test_score(user_id):
    pass


def is_has_innovation(user_id):
    pass


def is_has_academic(user_id):
    pass
