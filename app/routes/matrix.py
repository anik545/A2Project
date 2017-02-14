from flask import Flask,request,render_template,Blueprint
import flask
from ..pyscripts.matrices import Matrix
from fractions import Fraction

matrix_blueprint = Blueprint('matrix_blueprint',__name__,template_folder='templates')

@matrix_blueprint.route('/matrix', methods=['GET', 'POST'])
def matrix():
    result = None
    if request.method == 'POST':
        try:
            op = request.form.get('submit', None)
            acalc = request.form.get('a-submit', None)
            bcalc = request.form.get('b-submit', None)
            if acalc:
                letter = 'A'
                calc = acalc
            elif bcalc:
                letter = 'B'
                calc = bcalc
            else:
                mata = []
                for x in range(3): #TODO make a function def to get a matrix
                    mata.append([]) #def get_mat(letter,x,y):
                    for y in range(3):
                        string = 'A' + str(x) + str(y)
                        mata[x].append(Fraction(request.form[string]))
                matb = []
                for x in range(3):
                    matb.append([])
                    for y in range(3):
                        string = 'B' + str(x) + str(y)
                        matb[x].append(Fraction(request.form[string]))
                a = Matrix(mata)
                b = Matrix(matb)
                if op == 'X':
                    matresult = a * b
                if op == '-':
                    matresult = a - b
                if op == '+':
                    matresult = a + b
                result = matresult.tostr().rows
                return render_template('matrix.html', matrix_result=result, det_result=None, Error=None)

            mat = []
            for x in range(3):
                mat.append([])
                for y in range(3):
                    string = letter + str(x) + str(y)
                    mat[x].append(Fraction(request.form[string]))
            m = Matrix(mat)
            if 'Determinant' in calc:
                result = str(m.determinant())
                return render_template('matrix.html', matrix_result=None, det_result=result, Error=None)
            elif 'Inverse' in calc:
                result = m.inverse().tostr().rows
                return render_template('matrix.html', matrix_result=result, det_result=None, Error=None)
            elif 'Transpose' in calc:
                result = m.transpose().tostr().rows
                return render_template('matrix.html', matrix_result=result, det_result=None, Error=None)
            elif 'Triangle' in calc:
                result = m.triangle().tostr().rows
                return render_template('matrix.html', matrix_result=result, det_result=None, Error=None)

            else:
                return render_template('matrix.html', matrix_result=None, det_result=None, Error=None)
        except Exception as e:
            print(e)
            error = 'Invalid Matrix, Try again'
            return render_template('matrix.html', matrix_result=None, det_result=None, Error=error)

    return render_template('matrix.html', matrix_result=result)
