from sympy import im, re
import random
from cmath import phase

# https://pythonspot.com/factory-method/
class ComplexQuestion(object):
    """Class for creating matrix questions, inherits from BaseQuestion."""

    # @staticmethod
    # def factory(q_type):
    #     if q_type == 'add_sub':
    #         question, answer = add_sub_question(max_num)
    #         return ComplexQuestion(question,answer)
    #     other if statements
    # def __init__(self,question,answer)

    def __init__(self, q_type, max_num=10):
        self.question_type = q_type
        if q_type == 'add_sub':
            self.question, self.answer = add_sub_question(max_num)
        elif q_type == 'mul':
            self.question, self.answer = mult_question(max_num)
        elif q_type == 'div':
            self.question, self.answer = div_question(max_num)
        elif q_type == 'mod_arg':
            self.question, self.answer = mod_arg_question(max_num)

    def get_question(self):
        return self.question

    def get_answer(self):
        return self.answer


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
    print(ComplexQuestion('div').get_question())
