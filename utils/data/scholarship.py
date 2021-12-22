import get_rank_class
import get_score_pe
import is_innovation
import is_academic

from comments import learning_award_comments
from utils.comments import academic_excellence_award_comments, innovation_award_comments


def init_limit(person_name):
    score = get_score_pe(person_name)
    if score < 70:
        return False
    else:
        return True


def learning_award(user_id):
    rank = get_rank_class(user_id)
    return learning_award_comments(rank)


def innovation_award(user_id):
    is_award = is_innovation(user_id)
    return innovation_award_comments(is_award)


def academic_excellence_award(user_id):
    is_award = is_academic(user_id)
    return academic_excellence_award_comments(is_award)
