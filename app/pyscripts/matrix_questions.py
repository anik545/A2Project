from app.pyscripts.matrices import Matrix
import random

# TODO make parent class Matrix Question and subclasses for each question type
# TODO inverse question class with get_answer_float,get_answer_frac


class MatrixQuestion(object):
    """Class for creating matrix questions, inherits from BaseQuestion."""

    def __init__(self, q_type, small=True, size=3, max_num=10):
        self.question_type = q_type
        self.mat_ans = True
        if q_type == 'inv':
            self.question, self.answer = inv_question(size)
        elif q_type == 'det':
            self.mat_ans = False
            self.question, self.answer = det_question(size)
        elif q_type in ['sub', 'add', 'add_sub']:
            self.question, self.answer = add_sub_question(max_num, op=q_type)
        elif q_type == 'mul':
            self.question, self.answer = mult_question(small, max_num)
        else:
            raise ValueError

    def check_answer(self, ans):
        if ans == self.answer:
            return True
        else:
            return False

    def get_question(self):
        return self.question

    def get_answer(self):
        if self.question_type != 'det':
            return self.answer.get_rows()
        else:
            return self.answer

    def get_ans_dim(self):
        if type(self.answer) == Matrix:
            return self.answer.get_dimensions()
        else:
            return 0

def mult_question(small=True, max_num=10):
    s1 = (1, 2) if small else (3, 4)
    s2 = (2, 3) if small else (3, 4)
    y1 = random.randint(*s1)
    x1 = random.randint(*s2)
    y2 = x1
    x2 = random.randint(*s1)

    m1 = [[random.randint(1, max_num) for x in range(x1)] for y in range(y1)]
    m2 = [[random.randint(1, max_num) for x in range(x2)] for y in range(y2)]

    mat1 = Matrix(m1)
    mat2 = Matrix(m2)

    question = 'Calculate `' + str(m1) + '` X `' + str(m2)+'`'
    answer = (mat1 * mat2)
    return (question, answer)

def add_sub_question(max_num=10, op='add'):
    x, y = random.randint(2, 3), random.randint(2, 3)
    m1 = Matrix(
        [[random.randint(1, max_num) for x in range(x)] for y in range(y)]
            )
    m2 = Matrix(
        [[random.randint(1, max_num) for x in range(x)] for y in range(y)]
            )
    if op == 'add':
        answer = m1 + m2
        question = 'Calculate `'+str(m1.get_rows())+' + '+str(m2.get_rows())+'`'
    elif op == 'sub':
        answer = m1 - m2
        question = 'Calculate `'+str(m1.get_rows())+' - '+str(m2.get_rows())+'`'
    else:
        rand_op = random.choice(['+', '-'])
        if rand_op == '+':
            answer = m1 + m2
            question = 'Calculate `'+str(m1.get_rows())+' + '+str(m2.get_rows())+'`'
        else:
            answer = m1 - m2
            question = 'Calculate `' + str(m1.get_rows())+' - '+str(m2.get_rows()) + '`'
    return (question, answer)

def det_question(size=3):
    mat = Matrix(
        [[random.randint(1, 10) for x in range(size)] for y in range(size)]
            )
    answer = mat.determinant()
    question = 'Find the Determinant of `'+str(mat.get_rows())+'`'
    return (question, answer)

def inv_question(size=3):
    while True:
        mat = Matrix(
            [[random.randint(1, 10) for x in range(size)] for y in range(size)]
                )
        if mat.determinant() != 0:
            break
    answer = mat.inverse().tostr()
    question = 'Find the Inverse of `'+str(mat.get_rows())+'`'
    return (question, answer)

if __name__ == '__main__':
    qs = [MatrixQuestion(q_type='inv', size=4) for x in range(10)]
    for x in qs:
        print(x.get_question(), '---', x.get_answer())
