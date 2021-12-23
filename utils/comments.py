from utils.tools import _generate_comments_intro
from utils.data.scholarship import learning_award, innovation_award
from utils.data.credit import check_graduate, check_limited_major_subject_credict, check_arbitrary_major_subject_credict, check_general_elective_subject_credict


def wisdome_comment(score):
    if score > 95:
        return "你在智育积分上做的非常好，在科研方面可以更有所突出，争取发表顶会，顶刊等。"
    elif 85 < score < 95:
        return "你需要在成绩以及科研上有所提高，高年级时要多关注科研，轻竞赛和科研。"
    elif 75 < score <= 85:
        return "你需要加强你的基础知识，将成绩有所提高，科研方面量力而行。"
    elif score <= 75:
        return "希望你将心思放在学习上。"


def moral_comment(score):
    if score > 60:
        return "你是一个热爱社会，集体的人，希望你保持这般热忱继续奉献自己！"
    elif 30 < score <= 60:
        return "感谢你为集体，社会所做的贡献，你是一个善良的人。"
    elif 10 < score <= 30:
        return "参加了一定活动，趁着年轻再多做些工作！"
    elif score <= 10:
        return "希望你多多参加集体活动，大学期间多参加社会志愿服务是有必要的。"


def physical_comment(score):
    if score > 90:
        return " 你的身体素质非常强，可以向身边的人宣传下自己如何锻炼的，与大家一起锻炼。"
    elif 60 < score <= 90:
        return "你的身体素质保持的还可以，但还是希望能够坚持锻炼，身体是革命的本钱。"
    elif score <= 60:
        return "你的身体素质有些低，希望你多多锻炼，重视你的身体素质。"


def aesthetic_comment(score):
    if score > 56:
        return "你的爱好很广泛！希望继续保持！文艺汇演非你莫属！"
    elif 28 < score <= 56:
        return "拥有一两个爱好已经很棒了！希望继续保持！可以多多参加文艺汇演等活动"
    elif score <= 28:
        return "在大学期间要多培养自己的兴趣爱好，全面发展。"


def labor_comment(score):
    if score > 0:
        return "感谢你对集体，学生们做出的贡献，你在劳育的部分做的非常棒了，希望你能够平衡好学生工作与生活还有学业上的时间。"
    else:
        return "在大学期间可以适当参加学生工作，丰富自己的经历！"


def learning_award_comments(rank):
    if rank <= 6:
        return "你的排名是：" + str(rank) + "你可以获得校学习优秀奖。成绩不错，明年继续加油！"
    else:
        diff = rank - 6
        return "你的排名是：" + str(rank) + "你离参评校学习优秀奖还差" + str(diff) + "名，明年加油！"


def innovation_award_comments(is_award):
    if is_award == True:
        return "你在本学期可以获得创新创业奖。"
    else:
        return "你在本学期无法获得创新创业奖，你需要参加学校认定的学科竞赛或者发表论文，专利等。"


def academic_excellence_award_comments(is_award):
    if is_award == True:
        return "你在本学期可以获得学术卓越奖"
    else:
        return "你在本学期无法获得学术卓越奖，你需要拥有樊恭烋荣誉学院奖学金评定条例上的论文或专利。"


def compare_subject_comments(user1_name, user2_name, user1_subject_score, user2_subject_score, subject):
    diff = abs(user1_subject_score - user2_subject_score)
    if user1_subject_score < user2_subject_score:
        return user1_name + subject + "成绩比" + user2_name + "低" + str(diff)
    else:
        return user1_name + subject + "成绩比" + user2_name + "高" + str(diff)


def check_graduate_comments(all_credicts):
    if all_credicts >= 172:
        return "你的已修学分为" + str(all_credicts) + "，可以毕业。"
    else:
        return "你的已修学分为" + str(all_credicts) + "，不可以毕业，还差" + str(172 - all_credicts) + "学分。"


def check_limited_major_subject_credict_comments(limited_credit):
    if limited_credit < 6:
        return "你的已修专业限选课的学分为" + str(limited_credit) + "，需要再修" + str(6 - limited_credit) + "学分。"
    else:
        return "你的已修专业限选课的学分为" + str(limited_credit) + "，已满足樊恭烋荣誉学院专业限选课培养计划。"


def check_arbitrary_major_subject_credict_comments(arbitrary_credit):
    if arbitrary_credit < 4:
        return "你的已修专业任选课的学分为" + str(arbitrary_credit) + "，需要再修" + str(4 - arbitrary_credit) + "学分。"
    else:
        return "你的已修专业任选课的学分为" + str(arbitrary_credit) + "，已满足樊恭烋荣誉学院专业任选课培养计划。"


def check_general_elective_subject_credict_comments(general_elective_subject_credict):
    if general_elective_subject_credict < 8:
        return "你的已修通识教育选修课的学分为" + str(general_elective_subject_credict) + "，需要再修" + str(8 - general_elective_subject_credict) + "学分。"
    else:
        return "你的已修通识教育选修课的学分为" + str(general_elective_subject_credict) + "，已满足樊恭烋荣誉学院通识教育选修课培养计划。"


def composite_comments_intro(args):
    return "北京工业大学樊恭烋荣誉学院" + args['name'] + "同学你好，截止到目前为止你的加权平均分为" + \
            str(args['weighted_average_score']) + "。在班级" + str(args['class_num']) + "人数中的排名第" + str(args['rank']) + "。"


def composite_comments_award(user_id):
    return learning_award(user_id) + innovation_award(user_id)


def composite_comments_credit(user_id):
    return check_graduate(user_id) + check_limited_major_subject_credict(user_id) + check_arbitrary_major_subject_credict(user_id) \
            + check_general_elective_subject_credict_comments(user_id)


def composite_comments(user_id):
    args_intro = _generate_comments_intro(user_id)
    intro_comments = composite_comments_intro(args_intro)
    return intro_comments + composite_comments_award(user_id) + composite_comments_credit(user_id)
