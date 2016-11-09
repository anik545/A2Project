from flask import Flask,render_template,request,jsonify,abort
from complex_loci import *

from views.matrix import matrix_blueprint

app=Flask(__name__)
app.register_blueprint(matrix_blueprint)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/loci-plotter')
def loci():
    return render_template('loci.html')

@app.route('/_plot')
def plot():
    eq=request.args.get('eq',0,type=str)
    if 'arg' in eq:
        LHS,RHS=eq.split('=')
        p1,p2 = get_line_simple_arg(LHS,RHS)
        typ='ray'
        return jsonify(result=[p1,p2],type=typ)
    else:
        LHS,RHS=eq.split('=')
        typ,lines=get_lines(LHS,RHS)
        lines=[str(x).replace('**','^') for x in lines]
        print(typ,lines)
        if lines:
            return jsonify(result=lines,type=typ)
        else:
            abort(500)

@app.route('/operations-argand')
def operations():
    return render_template('operations.html')

@app.route('/ttt')
def ttt():
    return render_template('ttt.html')

if __name__=='__main__':
    app.debug = True
    app.run()
