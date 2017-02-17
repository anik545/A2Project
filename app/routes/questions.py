from flask import Flask, request, Blueprint, render_template, session, abort, jsonify, flash
from ..pyscripts.matrix_questions import MatrixQuestion
from ..pyscripts.complex_questions import ComplexQuestion
from ..pyscripts.question_dict import COMPLEX_QUESTIONS, MATRIX_QUESTIONS, QUESTIONS
import ast
from flask_login import current_user

from ..models import Mark, User, Student, Task, Teacher
from app import db

questions_blueprint = Blueprint('questions',__name__,template_folder='templates')

@questions_blueprint.route('/questions')
def questions():
    return render_template('questions/questions.html')

@questions_blueprint.route('/questions/<topic>/<q_type>')
def show_questions(topic,q_type):
    q_number = request.args.get('n',10)
    if topic == 'matrix':
        questions = [MatrixQuestion(q_type) for x in range(q_number)]
        answers = [q.get_answer() for q in questions]
        matans = questions[0].mat_ans
        session['questions'] = [q.get_question() for q in questions]
        session['answers'] = [str(q.get_answer()) for q in questions]
        return render_template('questions/mat_questions.html',questions=enumerate(questions),answers=answers,mat_ans=matans,q_type=q_type,topic=topic)
    elif topic == 'complex':
        questions = [ComplexQuestion(q_type) for x in range(q_number)]
        answers = [q.get_answer() for q in questions]
        session['questions'] = [q.get_question() for q in questions]
        session['answers'] = [str(q.get_answer()) for q in questions]
        return render_template('questions/complex_questions.html',questions=enumerate(questions),answers=answers,q_type=q_type,topic=topic)
    else:
        abort(404)

@questions_blueprint.route('/questions/_answers/<topic>/<q_type>')
def answers(topic,q_type):
    if topic == 'matrix':
        question_id = MATRIX_QUESTIONS[q_type]
        answers = session['answers']
        if q_type == 'det':
            question_id=3
            inputs = [request.form.get(str(x),0) for x in range(10)]
            inputs = [int(x) if x else 0 for x in inputs]
            scores = []
            for n,x in enumerate(answers):
                if x == inputs[n]:
                    scores.append(1)
                else:
                    scores.append(0)
            percent = sum(scores)*100//len(answers)
        else:
            answers = [[[str(i) for i in j] for j in ast.literal_eval(a)] for a in answers]
            inputs=[]
            for n,a in enumerate(answers):
                inputs.append([])
                for x in range(len(a)):
                    inputs[n].append([])
                    for y in range(len(a[0])):
                        i=request.args.get(str(n)+str(x)+str(y),0)
                        if i:
                            inputs[n][x].append(i)
                        else:
                            inputs[n][x].append('0')
            scores = []
            for n,x in enumerate(answers):
                if x == inputs[n]:
                    scores.append(1)
                else:
                    scores.append(0)
            percent = sum(scores)*100//len(answers)
        questions = session['questions']
        answers = [str(a).replace("'","") for a in answers]
        inputs = [str(i).replace("'","") for i in inputs]

    elif topic == 'complex':
        question_id = COMPLEX_QUESTIONS[q_type]
        answers = session['answers']
        if q_type == 'mod_arg':
            inputs = []
            for x in range(len(answers)):
                inputs.append((request.args.get(str(x)+'mod',0),request.args.get(str(x)+'arg',0)))
            answers = [(str(i),str(j)) for i,j in [ast.literal_eval(a) for a in answers]]
            scores=[]
            for n,x in enumerate(answers):
                if x==inputs[n]:
                    scores.append(1)
                else:
                    scores.append(0)
            percent=sum(scores)*100//len(answers)
            pass
        else:
            inputs = []
            for x in range(10):
                inputs.append(str(request.args.get(str(x)+'re',0))+'+'+str(request.args.get(str(x)+'im',0))+'j')
            scores=[]
            for n,x in enumerate(answers):
                print(x,'||',inputs[n])
                if complex(x) == complex(inputs[n]):
                    scores.append(1)
                else:
                    scores.append(0)
            percent = sum(scores)*100//len(answers)
        questions = session['questions']
        print(scores)
    else:
        abort(404)
    if current_user.is_authenticated and current_user.role == 'student':
        mark = Mark(sum(scores),len(scores),question_id,current_user.user_id)
        db.session.add(mark)
        s = Student.query.filter_by(user_id=current_user.user_id).first()
        ts = s.tasks.all()
        task = None
        for t in ts:
            if t.question_id == question_id:
                task = t
                break
        if task:
            task.mark_id = mark.mark_id
            task.completed = True
            db.session.add(task)
            flash('Task Completed!')
        db.session.commit()
    return jsonify(answers=answers,inputs=inputs,questions=questions,percent=percent,scores=scores)
