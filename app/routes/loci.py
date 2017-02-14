from flask import Flask, render_template, request, jsonify, abort, redirect, url_for, Blueprint
from flask_login import login_required, current_user

from ..pyscripts.complex_loci import *

from ..models import Graph, User
from app import db

loci_blueprint = Blueprint('loci',__name__,template_folder='templates')

@loci_blueprint.route('/loci-plotter')
def loci():
    if current_user.is_authenticated:
        user = User.query.get(current_user.user_id)
        user_graphs = user.graphs.all()
    else:
        user_graphs = None
    return render_template('loci.html',user_graphs=user_graphs)


@loci_blueprint.route('/_plot')
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

@loci_blueprint.route('/_addgraph',methods=['GET','POST'])
@login_required
def addgraph():
    if request.method=='POST':
        try:
            data1 = request.form.get('desmosdata',None)
            data2 = request.form.get('exprlist',None)
            title = request.form.get('title',"")
            desc = request.form.get('description',"")
            image_url = request.form.get('image',"")
            user_id = current_user.user_id
            print(type(Graph.query.filter_by(title=title,user_id=user_id).first()))
            exists = Graph.query.filter_by(title=title,user_id=user_id).first()
            if exists:
                return jsonify(status="error",error="Graph already exists")
            else:
                g=Graph(data1,data2,user_id,title,desc,image_url)
                db.session.add(g)
                db.session.commit()
                graph_id = g.graph_id #has to be after commit
                return jsonify(id=graph_id,title=title,image_url=image_url,desc=desc,status="ok",error=None)
        except Exception as e:
            print(e)
            return jsonify(status="error",error="Error saving Graph")
    if request.method=='GET':
        try:
            graph_id = request.args.get('graph_id',None)
            g = Graph.query.get(graph_id)
            return jsonify(desmosdata=g.desmosdata,exprlist=g.exprlist)
        except Exception as e:
            print(e)
            return abort(500)

@loci_blueprint.route('/operations-argand')
def operations():
    return render_template('operations.html')
