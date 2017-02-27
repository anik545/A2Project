from app.pyscripts.matrices import Matrix
from BaseQuestion import BaseQuestion
import random

class MatrixQuestion(BaseQuestion):
    """Class for creating matrix questions, inherits from BaseQuestion."""
    
    def get_answer(self):
        """Override get_answer as matrix type answers need to also call get_rows"""
        if self.question_type != 'det':
            return self.answer.get_rows()
        else:
            return self.answer

    def get_ans_dim(self):
        if type(self.answer) == Matrix:
            return self.answer.get_dimensions()
        else:
            return 0

    @staticmethod
    def get_question(q_type, small=True, size=3, max_num=10):
        if q_type == 'add_sub':
            question, answer = add_sub_question(max_num, op='add_sub')
        elif q_type == 'mul':
            question, answer = mult_question(small, max_num)
        elif q_type == 'inv':
            question, answer = inv_question(size)
        elif q_type == 'det':
            question, answer = det_question(size)
        return MatrixQuestion(question,answer,q_type)


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
