from utils.tools import get_all_credit, get_all_limited_credit, get_all_arbitrary_credit


def check_graduate(user_id):
    from utils.comments import check_graduate_comments
    all_credict = get_all_credit(user_id)
    return check_graduate_comments(all_credict)


def check_limited_major_subject_credict(user_id):
    from utils.comments import check_limited_major_subject_credict_comments
    limited_credit = get_all_limited_credit(user_id)
    return check_limited_major_subject_credict_comments(limited_credit)


def check_arbitrary_major_subject_credict(user_id):
    from utils.comments import check_arbitrary_major_subject_credict_comments
    arbitrary_credit = get_all_arbitrary_credit(user_id)
    return check_arbitrary_major_subject_credict_comments(arbitrary_credit)
