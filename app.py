from flask import Flask, render_template, request, jsonify, abort
from complex_loci import *
from matrix_questions import MatrixQuestion
from complex_questions import ComplexQuestion

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

@app.route('/questions/mat_questions')
def mat_questions():
    q_type = request.args.get('q_type',None)
    q_number = request.args.get('n',10)
    questions = [MatrixQuestion(q_type) for x in range(q_number)]
    return render_template('mat_questions.html',q_type=q_type,questions=enumerate(questions))

@app.route('/questions/complex_questions')
def complex_questions():
    q_type = request.args.get('q_type',None)
    q_number = request.args.get('n',10)
    questions = [ComplexQuestion(q_type) for x in range(q_number)]
    return render_template('complex_questions.html',q_type=q_type,questions=enumerate(questions))


@app.route('/ttt')
def ttt():
    return render_template('ttt.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
