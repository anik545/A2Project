class BaseQuestion(object):
    """Base question which matrix and complex question inherit from."""

    def __init__(self, question, answer, q_type):
        """Constructor for simple question object."""
        self.question = question
        self.answer = answer
        self.question_type = q_type

    def get_q(self):
        """Return question as string."""
        return str(self.question)

    def get_answer(self):
        """Return answer."""
        return self.answer
