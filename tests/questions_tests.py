from app.pyscripts.complex_questions import ComplexQuestion
from app.pyscripts.matrix_questions import MatrixQuestion


def test_complex_questions():
    for x in range(2):
        for question_type in ['add_sub', 'mult', 'div', 'mod_arg']:
            print(ComplexQuestion.get_question(question_type).get_q())
            print(ComplexQuestion.get_question(question_type).get_answer())
            print(ComplexQuestion.get_question(question_type).is_mod_arg())
            print('----')


def test_matrix_questions():
    for x in range(2):
        for question_type in ['add_sub', 'mult', 'det', 'inv']:
            print(MatrixQuestion.get_question(question_type).get_q())
            print(MatrixQuestion.get_question(question_type).get_answer())
            print(MatrixQuestion.get_question(question_type).is_mat_ans())
            print(MatrixQuestion.get_question(question_type).get_ans_dim())
            print('----')


test_complex_questions()
print('==============')
test_matrix_questions()
