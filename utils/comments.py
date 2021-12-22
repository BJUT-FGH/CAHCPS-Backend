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
