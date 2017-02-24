from flask import render_template, request, jsonify, abort, Blueprint
from flask_login import login_required, current_user

from ..pyscripts.complex_loci import get_implicit

from ..models import Graph, User
from app import db

import sympy as s

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

@loci_blueprint.route('/_addcalc',methods=['GET'])
def addcalc():
    eq_str = request.args.get('eq',None)
    points = request.args.get('points',None)
    eq = s.simpify(eq)
    vars_ = eq.free_symbols
    real = str(s.re(eq))
    imag = (s.im(eq))
    for v in vars_:
        real.replace('im('+str(v)')',str(v)+'.Y()')
        real.replace('re('+str(v)')',str(v)+'.X()')
        imag.replace('im('+str(v)')',str(v)+'.Y()')
        imag.replace('re('+str(v)')',str(v)+'.X()')
    return jsonify(point = {x:real,y:imag})
