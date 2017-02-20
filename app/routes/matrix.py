from flask import request, render_template, Blueprint
from ..pyscripts.matrices import Matrix
from fractions import Fraction

# Initialize blueprint
matrix_blueprint = Blueprint('matrix_blueprint', __name__,
                             template_folder='templates')


@matrix_blueprint.route('/matrix', methods=['GET', 'POST'])
def matrix():
    result = None
    # If the form is posted, it is submitted
    if request.method == 'POST':
        try:
            # Get operator pressed (+,-,*)
            # If no operator was pressed, op = None
            op = request.form.get('submit', None)
            # Get operation requested if a button under matrix A is pressed
            acalc = request.form.get('a-submit', None)
            # Get operation requested if a button under matrix A is pressed
            bcalc = request.form.get('b-submit', None)
            if acalc:
                # If operation on Matrix A requested
                letter = 'A'
                calc = acalc
            elif bcalc:
                # If operation on Matrix B requested
                letter = 'B'
                calc = bcalc
            else:
                # Initialise matrix A list
                mata = []
                # Get matrix data from form
                for x in range(3):  # TODO make a function def to get a matrix
                    mata.append([])  # def get_mat(letter,x,y):
                    for y in range(3):
                        string = 'A' + str(x) + str(y)
                        mata[x].append(Fraction(request.form[string]))
                # Initialise matrix B list
                matb = []
                # Get matrix data from form
                for x in range(3):
                    matb.append([])
                    for y in range(3):
                        string = 'B' + str(x) + str(y)
                        matb[x].append(Fraction(request.form[string]))
                # Create both matric objects
                a = Matrix(mata)
                b = Matrix(matb)
                # Check which operator button pressed
                # Assign result to matresult depending on operator
                if op == 'X':
                    matresult = a * b
                if op == '-':
                    matresult = a - b
                if op == '+':
                    matresult = a + b
                # Convert all items in matrix to strings and return page
                result = matresult.tostr().rows
                return render_template('matrix.html', matrix_result=result,
                                       det_result=None, Error=None)
            # Initialise Matrix list
            mat = []
            for x in range(3):
                mat.append([])
                for y in range(3):
                    # Get data from form for correct matrix
                    # Depends on whcih button was pressed
                    string = letter + str(x) + str(y)
                    mat[x].append(Fraction(request.form[string]))
            # Create matrix object based on this
            m = Matrix(mat)
            # Calculate result depending on which button pressed
            # Return page with result
            if 'Determinant' in calc:
                result = str(m.determinant())
                return render_template('matrix.html', matrix_result=None,
                                       det_result=result, Error=None)
            elif 'Inverse' in calc:
                result = m.inverse().tostr().rows
                return render_template('matrix.html', matrix_result=result,
                                       det_result=None, Error=None)
            elif 'Transpose' in calc:
                result = m.transpose().tostr().rows
                return render_template('matrix.html', matrix_result=result,
                                       det_result=None, Error=None)
            elif 'Triangle' in calc:
                result = m.triangle().tostr().rows
                return render_template('matrix.html', matrix_result=result,
                                       det_result=None, Error=None)

            else:
                return render_template('matrix.html', matrix_result=None,
                                       det_result=None, Error=None)
        except Exception as e:
            print(e)
            # If there was an error, return page with an error message
            error = 'Invalid Matrix, Try again'
            return render_template('matrix.html', matrix_result=None,
                                   det_result=None, Error=error)
    # Return basic page if GET request (no form submitted yet) 
    return render_template('matrix.html', matrix_result=result)
