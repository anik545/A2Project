from sympy import im, re
import random
from cmath import phase
from BaseQuestion import BaseQuestion


class ComplexQuestion(BaseQuestion):
    """Class for creating matrix questions, inherits from BaseQuestion."""

    @staticmethod
    def get_question(q_type, max_num=10):
        if q_type == 'add_sub':
            question, answer = add_sub_question(max_num)
        elif q_type == 'mul':
            question, answer = mult_question(max_num)
        elif q_type == 'div':
            question, answer = div_question(max_num)
        elif q_type == 'mod_arg':
            question, answer = mod_arg_question(max_num)
        return ComplexQuestion(question,answer,q_type)

    def is_mod_arg(self):
        if self.question_type == 'mod_arg':
            return True
        else:
            return False


def add_sub_question(maxnum=10):
    a = random.randint(1, 10) + random.randint(1, 10) * 1j
    b = random.randint(1, 10) + random.randint(1, 10) * 1j
    rand_op = random.choice(['+', '-'])
    if rand_op == '+':
        answer = a+b
        question = "Calculate  `" + str(a).replace('j', 'i') + "` + `"+str(b).replace('j', 'i') + "`"
    else:
        answer = a-b
        question = "Calculate  `" + str(a).replace('j', 'i') + "` - `"+str(b).replace('j', 'i') + "`"
    return (question, answer)


def mult_question(maxnum=10):
    a = random.randint(1, maxnum) + random.randint(1, maxnum) * 1j
    b = random.randint(1, maxnum) + random.randint(1, maxnum) * 1j
    ans = a * b
    answer = im(ans) * 1j + re(ans)
    question = "Calculate  `" + str(a).replace('j', 'i') + "` * `"+str(b).replace('j', 'i') + "`"
    return (question, answer)


def div_question(maxnum=10):
    a = random.randint(1, maxnum) + random.randint(1, maxnum) * 1j
    b = random.randint(1, maxnum) + random.randint(1, maxnum) * 1j
    ans = a / b
    answer = round(im(ans), 2) * 1j + round(re(ans), 2)
    question = "Calculate `" + str(a).replace('j', 'i') + " / "+str(b).replace('j', 'i') + "` (2 decimal places)"
    return (question, answer)


def mod_arg_question(maxnum=10):
    a = random.randint(1, maxnum)+random.randint(1, maxnum) * 1j
    mod = round(abs(a), 2)
    arg = round(phase(a), 2)
    answer = (mod, arg)
    question = 'Find, to two decimal places, the modulus and argument of  `'+str(a).replace('j', 'i')+'`'
    return (question, answer)


if __name__ == '__main__':
    print(ComplexQuestion.get_question('add_sub').get_q())
