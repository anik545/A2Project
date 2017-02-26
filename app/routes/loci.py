from flask import render_template, request, jsonify, abort, Blueprint
from flask_login import login_required, current_user

from ..pyscripts.complex_loci import get_implicit

from ..models import Graph, User
from app import db

from sympy import sympify, re, im

# Initialise blueprint
loci_blueprint = Blueprint('loci', __name__, template_folder='templates')


@loci_blueprint.route('/loci-plotter')
def loci():
    if current_user.is_authenticated:
        # If user is logged in, load and send saved graph data
        user = User.query.get(current_user.user_id)
        user_graphs = user.graphs.all()
    else:
        user_graphs = None
    return render_template('loci.html', user_graphs=user_graphs)


@loci_blueprint.route('/_plot')
def plot():
    # Get input equation
    eq = request.args.get('eq', 0, type=str)
    try:
        # Modify equation with function in complex_loci.py
        line = get_implicit(eq, latx=True)
        if ' i ' in line:
            # A separated i means that there is a complex number in the output
            # This means the input equation was invalid
            raise TypeError
        return jsonify(result=line)
    except Exception as e:
        # Abort if there is an error (causes error message on client-side)
        abort(500)


@loci_blueprint.route('/_addgraph', methods=['GET', 'POST'])
@login_required
def addgraph():
    if request.method == 'POST':
        # POST request means user is saving a graph
        try:
            # Get data from form
            data1 = request.form.get('desmosdata', None)
            data2 = request.form.get('exprlist', None)
            title = request.form.get('title', "")
            desc = request.form.get('description', "")
            image_url = request.form.get('image', "")
            user_id = current_user.user_id

            exists = Graph.query.filter_by(
                title=title, user_id=user_id).first()
            if exists:
                # Prevent same graph getting saved more than once
                return jsonify(status="error", error="Graph already exists")
            else:
                # Add graph data to database and link to current user
                g = Graph(data1, data2, user_id, title, desc, image_url)
                db.session.add(g)
                db.session.commit()
                graph_id = g.graph_id  # has to be after commit
                return jsonify(id=graph_id, title=title, image_url=image_url,
                               desc=desc, status="ok", error=None)
        except Exception as e:
            # Return error message and error status if there is an error
            # Causes error popup on client-side
            return jsonify(status="error", error="Error saving Graph")
    if request.method == 'GET':
        # GET request means the user is loading a graph
        try:
            graph_id = request.args.get('graph_id', None)
            g = Graph.query.get(graph_id)
            return jsonify(desmosdata=g.desmosdata, exprlist=g.exprlist)
        except Exception as e:
            # Abort if there is an error (causes error message on client-side)
            return abort(500)


@loci_blueprint.route('/operations-argand')
def operations():
    return render_template('operations.html')


@loci_blueprint.route('/_addcalc', methods=['GET'])
def addcalc():
    # Get equation requested
    eq_str = request.args.get('eq', None)
    # Convert to sympy object
    eq = sympify(eq_str)
    # Get all the variables in the expression
    vars_ = eq.free_symbols
    # get real and imaginary parts of expression
    real = str(re(eq).expand(complex=True))
    imag = str(im(eq).expand(complex=True))
    # Loop over the variables
    for v in vars_:
        # Replace im(variable) with variable.Y()
        # Replace re(variable) with variable.X()
        # This is how JSXGraph allows points based on other points
        real = real.replace('im('+str(v)+')', str(v)+'.Y()')
        real = real.replace('re('+str(v)+')', str(v)+'.X()')
        imag = imag.replace('im('+str(v)+')', str(v)+'.Y()')
        imag = imag.replace('re('+str(v)+')', str(v)+'.X()')
    # Relace functions for javascript
    real = real.replace('**', '^').replace('sin', 'Math.sin').replace('cos',  'Math.cos').replace('atan2', 'Math.atan')
    imag = imag.replace('**', '^').replace('sin', 'Math.sin').replace('cos',  'Math.cos').replace('atan2', 'Math.atan')
    # Return the real and imaginary parts of calculated points as JSON
    return jsonify(x=real, y=imag)
