import ast

from flask import (Blueprint, abort, flash, jsonify, render_template,
                   request, session)
from flask_login import current_user

from app import db

from ..models import Mark, Student
from ..pyscripts.complex_questions import ComplexQuestion
from ..pyscripts.matrix_questions import MatrixQuestion
from ..pyscripts.question_dict import COMPLEX_QUESTIONS, MATRIX_QUESTIONS

# Initialise Blueprint
questions_blueprint = Blueprint('questions', __name__,
                                template_folder='templates')


@questions_blueprint.route('/questions')
def questions():
    """Questions home page."""
    return render_template('questions/questions.html')


@questions_blueprint.route('/questions/<topic>/<q_type>')
def show_questions(topic, q_type):
    """Show page with requested question type."""
    q_number = request.args.get('n', 10)
    if topic == 'matrix':
        # Generate question objects
        questions = [MatrixQuestion(q_type) for x in range(q_number)]
        # Get list of answers from question objects
        answers = [q.get_answer() for q in questions]
        # Check whether the answers are of type matrix or not
        matans = questions[0].mat_ans
        # List of question strings from question objects
        # List of answer strings from question objects
        # Save both in server side session
        session['questions'] = [q.get_question() for q in questions]
        session['answers'] = [str(q.get_answer()) for q in questions]
        return render_template('questions/mat_questions.html',
                                questions=enumerate(questions), answers=answers,
                                mat_ans=matans, q_type=q_type, topic=topic)
    elif topic == 'complex':
        questions = [ComplexQuestion(q_type) for x in range(q_number)]
        answers = [q.get_answer() for q in questions]
        session['questions'] = [q.get_question() for q in questions]
        session['answers'] = [str(q.get_answer()) for q in questions]
        return render_template('questions/complex_questions.html',
                                questions=enumerate(questions), answers=answers,
                                q_type=q_type, topic=topic)
    else:
        # If topic is invalid, return 404 page not found
        abort(404)


@questions_blueprint.route('/questions/_answers/<topic>/<q_type>')
def answers(topic, q_type):
    """Return scores and marked questions given topic, question type and list
    of input answers from questions form"""
    if topic == 'matrix':
        # Get question_id from dictionary
        question_id = MATRIX_QUESTIONS[q_type]
        # Get answers from session
        answers = session['answers']
        if q_type == 'det':
            # For determinant questions (non-matrix answers)
            # Get all input answers from form
            inputs = [request.form.get(str(x), 0) for x in range(10)]
            # Convert all inputs to ints
            inputs = [int(x) if x else 0 for x in inputs]
            # Initialise empty scores array
            scores = []
            # Loop over all answers
            for n, x in enumerate(answers):
                # check corresponding input answer
                # Add one to scores array if input answer matches
                if x == inputs[n]:
                    scores.append(1)
                else:
                    scores.append(0)
            # Calculate percentage score
            percent = sum(scores)*100//len(answers)
        else:
            # Convert each answer in answers list to a 2-d list
            # Also convert all elements in matrix to string
            answers = [[[str(i) for i in j] for j in ast.literal_eval(a)] for a in answers]
            # Initialize input answers list
            inputs = []
            for n, a in enumerate(answers):
                inputs.append([])
                for x in range(len(a)):
                    inputs[n].append([])
                    for y in range(len(a[0])):
                        # Get form input and add to matrix
                        # Add 0 if there is no form input
                        i = request.args.get(str(n) + str(x) + str(y), 0)
                        if i:
                            inputs[n][x].append(i)
                        else:
                            inputs[n][x].append('0')
            # Initialise scores list
            scores = []
            # Check all input answers against stored answers
            for n, x in enumerate(answers):
                if x == inputs[n]:
                    scores.append(1)
                else:
                    scores.append(0)
            # Calculate percent score
            percent = sum(scores) * 100 // len(answers)
        questions = session['questions']
        # Convert items in answers and inputs to strings
        # so they can be displayed in score page
        answers = [str(a).replace("'", "") for a in answers]
        inputs = [str(i).replace("'", "") for i in inputs]

    elif topic == 'complex':
        # Get question id (for database)
        question_id = COMPLEX_QUESTIONS[q_type]
        answers = session['answers']
        if q_type == 'mod_arg':
            # For modulus and argument questions (non-complex answers)
            # Initialise input answer list
            inputs = []
            for x in range(len(answers)):
                # Get form inputs with names beginning mod and arg
                # Put into tuple (modulus,answer) and add to inputs list
                inputs.append((
                    request.args.get(str(x) + 'mod', 0),
                    request.args.get(str(x) + 'arg', 0)
                    ))
            # Change answers stored in session to correct type
            answers = [(str(i), str(j)) for i, j in [ast.literal_eval(a) for a in answers]]
            # Initialise scores list
            scores = []
            # Check answers, add 1 to scores if answers match else add 0
            for n, x in enumerate(answers):
                if x == inputs[n]:
                    scores.append(1)
                else:
                    scores.append(0)
            # Calculate percent score
            percent = sum(scores) * 100 // len(answers)
            pass
        else:
            # Initialise input answers list
            inputs = []
            for x in range(len(answers)):
                # Get form inputs
                # Add string representation of complex number answer to inputs
                inputs.append(
                    str(request.args.get(str(x)+'re', 0)) + '+' +
                    str(request.args.get(str(x) + 'im', 0))+'j')
            # Initialise scores list
            scores = []
            # Loop over answers
            for n, x in enumerate(answers):
                # Convert both input answer and stored answer to complex number
                # Check if both answers match and add 1 or 0 to scores
                if complex(x) == complex(inputs[n]):
                    scores.append(1)
                else:
                    scores.append(0)
            # Calculate percent score
            percent = sum(scores)*100//len(answers)
        questions = session['questions']
    else:
        # If topic is not matrix or complex, return 404
        abort(404)
    if current_user.is_authenticated and current_user.role == 'student':
        # Only add a mark to database if user is a logged in student
        mark = Mark(sum(scores), len(scores), question_id, current_user.user_id)
        db.session.add(mark)
        # Get student by user id
        s = Student.query.filter_by(user_id=current_user.user_id).first()
        # Get all of the students tasks
        ts = s.tasks.all()
        # Find out whether there is an active task with the same question_id
        # as the task that is being completed
        task = None
        # Loop over all tasks
        for t in ts:
            if t.question_id == question_id and t.completed is False:
                task = t
                # Break once relevant task found
                break
        # If there is no task, task = None
        # If there is such a task
        if task:
            # Link task with corresponding mark
            task.mark_id = mark.mark_id
            # Set task as completed
            task.completed = True
            # Add to database
            db.session.add(task)
            flash('Task Completed!')
        # Update database with all changes
        db.session.commit()
    # Return data in JSON form for javascript to display
    return jsonify(answers=answers, inputs=inputs, questions=questions,
                    percent=percent, scores=scores)
