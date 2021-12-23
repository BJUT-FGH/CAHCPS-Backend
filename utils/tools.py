from model import *
from utils.comments import composite_comments


def get_user_name(user_id):
    return User.get_by_id(user_id).name


def _get_subject_id(subject_name):
    return Subject.get(Subject.name == subject_name).subject_id


def _get_class_from_user(user_id):
    return User.select().where(User.uid == user_id).class_id


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


def _get_weighted_average(user_id):
    all_grade = _get_all_grade_w_weight(user_id)
    return round(_calc_weighted_average(all_grade), 2)


def _calc_credit_from_type(all_grade, type):
    all_credit = 0
    for g in all_grade:
        if g['type'] == type:
            all_credit += g['credit']
    return all_credit


def _calc_all_credit(all_grade):
    all_credit = 0
    for g in all_grade:
        all_credit += g['credit']
    return all_credit


def _get_class_list_user_id(class_id):
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
    class_id = _get_class_from_user(user_id)
    class_user_id = _get_class_list_user_id(class_id)
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


def get_all_credit(user_id):
    all_grade = _get_all_grade_w_weight(user_id)
    return _calc_all_credit(all_grade)


def get_all_limited_credit(user_id):
    all_grade = _get_all_grade_w_weight(user_id)
    limited_credit = _calc_credit_from_type(all_grade, SubjectType.专业限选课)
    return limited_credit


def get_all_arbitrary_credit(user_id):
    all_grade = _get_all_grade_w_weight(user_id)
    arbitrary_credit = _calc_credit_from_type(all_grade, SubjectType.专业任选课)
    return arbitrary_credit


def _get_class_num(class_id):
    class_user_id = _get_class_list_user_id(class_id)
    return len(class_user_id)


def _generate_comments_intro(user_id):
    args = {"name":"", "weighted_average_score":"", "class_num":0, "rank":0}
    args['name'] = get_user_name(user_id)
    args['weighted_average_score'] = _get_weighted_average(user_id)
    class_id = _get_class_from_user(user_id)
    args['class_num'] = _get_class_num(class_id)
    args['rank'] = get_rank_from_class(user_id)
    return args


def sum_up(user_id):
    return composite_comments(user_id)
