class BaseQuestion(object):

    def __init__(self,question,answer,q_type):
        self.question = question
        self.answer = answer
        self.question_type = q_type

    def get_q(self):
        return self.question

    def get_ans(self):
        return self.answer

    def check_answer(self, ans):
        if ans == self.answer:
            return True
        else:
            return False
