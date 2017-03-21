from app.pyscripts.matrices import Matrix
from app.pyscripts.base_question import BaseQuestion
import random


class MatrixQuestion(BaseQuestion):
    """Class for creating matrix questions, inherits from BaseQuestion."""

    @staticmethod
    def get_question(q_type):
        """Return matrix question object given question type."""
        if q_type == 'add_sub':
            question, answer = add_sub_question()
        elif q_type == 'mult':
            question, answer = mult_question()
        elif q_type == 'inv':
            question, answer = inv_question()
        elif q_type == 'det':
            question, answer = det_question()
        else:
            raise ValueError
        return MatrixQuestion(question, answer, q_type)

    def get_answer(self):
        """Override get_answer as matrix type answers need to also call get_rows."""
        if self.question_type != 'det':
            return self.answer.get_rows()
        else:
            return self.answer

    def is_mat_ans(self):
        """Return True if answer is a matrix."""
        if type(self.answer) != Matrix:
            return False
        else:
            return True

    def get_ans_dim(self):
        """Return dimensions if answer is a matrix, otherwise return 0."""
        if type(self.answer) == Matrix:
            return self.answer.get_dimensions()
        else:
            return 0


def mult_question():
    """Return random question and answer pair for multiplication."""
    # Choose a random size for first matrix
    y1 = random.randint(1, 2)
    x1 = random.randint(2, 3)
    # Set height of second to width of first
    y2 = x1
    # Set random width of second matrix
    x2 = random.randint(1, 2)
    # Populate both matrices with random numbers (between 0 and 10)
    m1 = [[random.randint(1, 10) for x in range(x1)] for y in range(y1)]
    m2 = [[random.randint(1, 10) for x in range(x2)] for y in range(y2)]
    # Create matrix objects from the 2D lists
    mat1 = Matrix(m1)
    mat2 = Matrix(m2)
    # Calculate answer and generate question
    question = 'Calculate `' + str(m1) + '` X `' + str(m2)+'`'
    answer = (mat1 * mat2)
    return (question, answer)


def add_sub_question():
    """Return random question and answer pair for addition and subtraction."""
    x, y = random.randint(2, 3), random.randint(2, 3)
    m1 = Matrix(
        [[random.randint(1, 10) for x in range(x)] for y in range(y)]
            )
    m2 = Matrix(
        [[random.randint(1, 10) for x in range(x)] for y in range(y)]
            )
    rand_op = random.choice(['+', '-'])
    # Calculate answer and create question based on which opertor was chosen
    if rand_op == '+':
        answer = m1 + m2
        question = 'Calculate `'+str(m1.get_rows())+' + '+str(m2.get_rows())+'`'
    else:
        answer = m1 - m2
        question = 'Calculate `' + str(m1.get_rows())+' - '+str(m2.get_rows()) + '`'
    return (question, answer)


def det_question():
    """Return random question and answer pair for finding the determinant."""
    # Generate randomly 3x3 matrix
    mat = Matrix(
        [[random.randint(1, 10) for x in range(3)] for y in range(3)]
            )
    # Calculate answer and generate question
    answer = mat.determinant()
    question = 'Find the Determinant of `'+str(mat.get_rows())+'`'
    return (question, answer)


def inv_question():
    """Return random question and answer pair for finding the inverse."""
    # Generate random matrices until one with an inverse is found
    while True:
        # Create random 3x3 matrix
        mat = Matrix(
            [[random.randint(1, 10) for x in range(3)] for y in range(3)]
            )
        if mat.determinant() != 0:
            # If Matrix with valid inverse is created, break
            break
    # Calculate answer and generate question
    question = 'Find the Inverse of `'+str(mat.get_rows())+'`'
    answer = mat.inverse().tostr()
    return (question, answer)

if __name__ == '__main__':
    q = MatrixQuestion.get_question('inv')
    print(q.get_q())
