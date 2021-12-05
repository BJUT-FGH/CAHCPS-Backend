

class Student():

    def __init__(self, name, grade):
        self.name = name
        self.grade = grade
        self.transcript = {}

    def change_gpa(self, new_gpa):
        self.gpa = new_gpa

    def change_grade(self, new_grade):
        self.grade = new_grade
    
    def change_paper_num(self, new_paper_num):
        self.paper_num = new_paper_num
    
    def get_course_score(self, course):
        return self.transcript[course]

    def eval(self):
        pass



# A = Student(1, 1)
# A.change_paper_published()
# print(A.paper_publish)

