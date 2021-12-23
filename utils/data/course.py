from utils.tools import get_subject_score, get_user_name
from utils.comments import compare_subject_comments


def compare_subject_score(user1_id, user2_id, subject):
    user1_subject_score = get_subject_score(user1_id, subject)
    user2_subject_score = get_subject_score(user2_id, subject)
    user1_name = get_user_name(user1_id)
    user2_name = get_user_name(user2_id)
    return compare_subject_comments(user1_name, user2_name, user1_subject_score, user2_subject_score, subject)
