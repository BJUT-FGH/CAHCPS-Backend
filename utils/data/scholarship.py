from utils.tools import get_pe_test_score, get_rank_from_class, is_has_academic, is_has_innovation
from utils.comments import learning_award_comments, academic_excellence_award_comments, innovation_award_comments


def init_limit(user_id):
    score = get_pe_test_score(user_id)
    return score >= 70


def learning_award(user_id):
    rank = get_rank_from_class(user_id)
    return learning_award_comments(rank)


def innovation_award(user_id):
    is_award = is_has_innovation(user_id)
    return innovation_award_comments(is_award)


def academic_excellence_award(user_id):
    is_award = is_has_academic(user_id)
    return academic_excellence_award_comments(is_award)
