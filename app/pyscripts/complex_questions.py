from sympy import im, re
import random
from cmath import phase
from app.pyscripts.base_question import BaseQuestion


class ComplexQuestion(BaseQuestion):
    """Class for creating matrix questions, inherits from BaseQuestion."""

    @staticmethod
    def get_question(q_type):
        """Return a question object given a question type."""
        if q_type == 'add_sub':
            question, answer = add_sub_question()
        elif q_type == 'mult':
            question, answer = mult_question()
        elif q_type == 'div':
            question, answer = div_question()
        elif q_type == 'mod_arg':
            question, answer = mod_arg_question()
        else:
            raise ValueError
        return ComplexQuestion(question, answer, q_type)

    def is_mod_arg(self):
        """Return true if the object is a modulus argument question."""
        if self.question_type == 'mod_arg':
            return True
        else:
            return False


def add_sub_question():
    """Return random question and answer pair for addition and subtraction."""
    # Generate 2 random complex numbers
    a = random.randint(1, 10) + random.randint(1, 10) * 1j
    b = random.randint(1, 10) + random.randint(1, 10) * 1j
    # Choose random operatot
    rand_op = random.choice(['+', '-'])
    # Calculate answer and create question based on which opertor was chosen
    if rand_op == '+':
        answer = a+b
        question = "Calculate  `" + str(a).replace('j', 'i') + "` + `"+str(b).replace('j', 'i') + "`"
    else:
        answer = a-b
        question = "Calculate  `" + str(a).replace('j', 'i') + "` - `"+str(b).replace('j', 'i') + "`"
    return (question, answer)


def mult_question():
    """Return random question and answer pair for multiplication."""
    # Generate 2 random complex numbers
    a = random.randint(1, 10) + random.randint(1, 10) * 1j
    b = random.randint(1, 10) + random.randint(1, 10) * 1j
    # Calculate answer and generate question with the random numbers
    answer = a * b
    question = "Calculate  `" + str(a).replace('j', 'i') + "` * `"+str(b).replace('j', 'i') + "`"
    return (question, answer)


def div_question():
    """Return random question and answer pair for division."""
    # Generate 2 random complex numbers
    a = random.randint(1, 10) + random.randint(1, 10) * 1j
    b = random.randint(1, 10) + random.randint(1, 10) * 1j
    # Calculate answer and generate question with the random numbers
    ans = a / b
    # Round both parts to 2 dp
    answer = round(im(ans), 2) * 1j + round(re(ans), 2)
    question = "Calculate `" + str(a).replace('j', 'i') + " / "+str(b).replace('j', 'i') + "` (2 decimal places)"
    return (question, answer)


def mod_arg_question():
    """Return random question and answer pair for modulus and argument."""
    # Generate 2 random complex numbers
    a = random.randint(1, 10)+random.randint(1, 10) * 1j
    # Calculate answer and generate question with the random numbers
    mod = round(abs(a), 2)   # Round both to two dp
    arg = round(phase(a), 2)
    answer = (mod, arg)
    question = 'Find, to two decimal places, the modulus and argument of  `'+str(a).replace('j', 'i')+'`'
    return (question, answer)


if __name__ == '__main__':
    print(ComplexQuestion.get_question('mult').get_answer())
