from flask import Flask, render_template, request, jsonify, abort
from complex_loci import *
from matrix_questions import MatrixQuestion
from complex_questions import ComplexQuestion

import ast

from views.matrix import matrix_blueprint

app = Flask(__name__)
app.register_blueprint(matrix_blueprint)


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/loci-plotter')
def loci():
    return render_template('loci.html')


@app.route('/_plot')
def plot():
    eq = request.args.get('eq', 0, type=str)
    try:
        line = get_implicit(eq, latx=True)
        print(line)
        if ' i ' in line:
            print('i in line')
            raise TypeError
        print(line)
        return jsonify(result=line)
    except Exception as e:
        print(e)
        abort(500)


@app.route('/operations-argand')
def operations():
    return render_template('operations.html')

@app.route('/questions')
def questions():
    return render_template('questions.html')

@app.route('/questions/<topic>/<q_type>')
def show_questions(topic,q_type):
    q_number = request.args.get('n',10)
    if topic == 'matrix':
        questions = [MatrixQuestion(q_type) for x in range(q_number)]
        answers = [q.get_answer() for q in questions]
        matans=questions[0].mat_ans
        return render_template('mat_questions.html',questions=enumerate(questions),answers=answers,mat_ans=matans)
    elif topic == 'complex':
        questions = [ComplexQuestion(q_type) for x in range(q_number)]
        answers = [q.get_answer() for q in questions]
        return render_template('complex_questions.html',questions=enumerate(questions),answers=answers)
    else:
        abort(404)


@app.route('/questions/answers/<topic>',methods=['GET','POST'])
def show_answers(topic):
    if topic == 'matrix':
        answers = request.args.getlist('ans',None)
        mat_ans = request.args.get('mat_ans','True')
        if mat_ans == 'True':
            answers = [ast.literal_eval(a) for a in answers]
            inputs=[]
            for n,a in enumerate(answers):
                inputs.append([])
                for x in range(len(a)):
                    inputs[n].append([])
                    for y in range(len(a[0])):
                        inputs[n][x].append(request.form.get(str(a)+str(x)+str(y),0))
        else:
            inputs = [request.form.get(str(x),0) for x in range(10)]
        print(inputs)
        print(answers)
        return render_template('answers.html',ans=answers,ins=enumerate(inputs))

    if topic == 'complex':
        answers = request.args.getlist('ans',None)
        inputs=[]
        for x in range(10):
            inputs.append((request.form.get(str(x)+'im',0),request.form.get(str(x)+'re',0)))
        print(inputs)
        print(answers)
        return render_template('answers.html',ans=answers,ins=inputs)
    else:
        abort(404)


@app.route('/ttt')
def ttt():
    return render_template('ttt.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
