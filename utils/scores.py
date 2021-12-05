from utils.comments import wisdome_comment, moral_comment, physical_comment, aesthetic_comment, labor_comment

w_rank_list = ["国际级", "国家级", "省级", "校级", "无"]
w_rank_score = [90, 80, 50, 30, 0]
w_grade = [1.4, 1.35, 1.3, 1.2]

w_wavg_weighted = 0.65
w_rank_weighted = 0.1
w_num_research_weighted = 0.25
w_research_basic = 10

m_activity_basic = 10

p_course_score_weighted = 0.8
p_num_phy_weighted = 0.2

a_num_hobby_basic = 20

l_union_worker_basic = 25
l_meida_worker_basic = 25
l_class_worker_basic = 25


def grade_avg(ret, grade):
    return ret * w_grade[grade - 1]


def wisdom_score(wavg, rank, num_research, grade=1):
    ret = 0
    ret += wavg * w_wavg_weighted
    ret += w_rank_score[w_rank_list.index(rank)] * w_rank_weighted
    ret += num_research * w_research_basic * w_num_research_weighted
    ret = round(grade_avg(ret, grade), 2)
    return ret, wisdome_comment(ret)


def moral_score(num_activity, grade=1):
    ret = 0
    ret += num_activity * m_activity_basic
    ret = round(grade_avg(ret, grade), 2)
    return ret, moral_comment(ret)


def physical_score(course_score, num_phy, grade=1):
    ret = 0
    ret += p_course_score_weighted * course_score
    ret += num_phy * p_num_phy_weighted
    ret = round(grade_avg(ret, grade), 2)
    return ret, physical_comment(ret)


def aesthetic_score(num_hobby, grade=1):
    ret = 0
    ret += num_hobby * a_num_hobby_basic
    ret = round(grade_avg(ret, grade), 2)
    return ret, aesthetic_comment(ret)


def labor_score(is_union_worker=True, is_meida_worker=True, is_class_worker=True, grade=1):
    ret = 0
    if is_union_worker:
        ret += l_union_worker_basic
    if is_meida_worker:
        ret += l_meida_worker_basic
    if is_class_worker:
        ret += l_class_worker_basic
    ret = 0 if ret == 0 else 100
    return ret, labor_comment(ret)


def composite_score(wisdom, moral, physical, aesthetic, labor):
    return wisdom * 0.5 + moral * 0.3 + physical * 0.1 + aesthetic * 0.05 + labor * 0.05


if __name__ == '__main__':
    w, _ = wisdom_score(85, "无", 0, grade=1)
    m, _ = moral_score(5, grade=1)
    p, _ = physical_score(96, 1, grade=1)
    a, _ = aesthetic_score(2, grade=1)
    l, _ = labor_score(is_union_worker=True, is_meida_worker=False, is_class_worker=False, grade=1)
    print("智育：", wisdom_score(85, "无", 0, grade=1))
    print("德育：", moral_score(5, grade=1))
    print("体育：", physical_score(96, 1, grade=1))
    print("美育：", aesthetic_score(2, grade=1))
    print("劳育：", labor_score(is_union_worker=True, is_meida_worker=False, is_class_worker=False, grade=1))
    print(composite_score(w, m, p, a, l))
